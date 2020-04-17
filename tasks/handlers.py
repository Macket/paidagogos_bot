from bot import bot
from users.models import Teacher, Student
from tasks.models import Task, Submission, SubmissionStatus
from tasks import markups
from datetime import datetime, timezone
from classrooms.views import classroom_detail_view
from tasks.views import task_detail_view, task_message_list_view, submission_list_view
from utils.scripts import get_call_data


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@TASK/'))
def handle_task_query(call):
    data = get_call_data(call)
    task_detail_view(call.message, data['task_id'], edit=True)


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@SUBMISSIONS/'))
def handle_submissions_query(call):
    data = get_call_data(call)
    submission_list_view(call.message, data['task_id'], edit=True)


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@TASK_MESSAGES/'))
def handle_task_messages_query(call):
    data = get_call_data(call)
    task_message_list_view(call.message, data['task_id'])
    task_detail_view(call.message, data['task_id'])


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@NEW_TASK/'))
def handle_new_task_query(call):
    data = get_call_data(call)
    task_name_request(call.message, data['classroom_id'])


def task_name_request(message, classroom_id):
    teacher = Teacher.get(message.chat.id)

    ru_text = "Отправьте название задания, например, «*Десятичные дроби*».\n\n" \
              "_Подсказка_: не включайте в название дату, это будет сделано автоматически."
    en_text = None
    text = ru_text if teacher.language_code == 'ru' else en_text

    bot.send_message(message.chat.id,
                     text,
                     # reply_markup=markups.get_compose_task_markup(teacher),  TODO Добавить автоматически сгенерированное задание
                     parse_mode='Markdown')
    bot.register_next_step_handler(message, task_name_receive, classroom_id)


def task_name_receive(message, classroom_id):
    teacher = Teacher.get(message.chat.id)

    task = Task(classroom_id, message.text, datetime.now(timezone.utc)).save()

    ru_text = "Отправьте мне задание в любом формате: " \
              "текст, фото, видео, файлы или аудиосообщения; одним или несколькими сообщениями.\n\n" \
              "Когда закончите, просто нажмите кнопку *Выдать задание* и я отправлю его ученикам"
    en_text = None
    text = ru_text if teacher.language_code == 'ru' else en_text

    bot.send_message(message.chat.id,
                     text,
                     reply_markup=markups.get_compose_task_markup(teacher),
                     parse_mode='Markdown')
    bot.register_next_step_handler(message, compose_task, task)


def compose_task(message, task):
    if message.text in ['Выдать задание', 'Assign task']:
        bot.send_message(message.chat.id, 'Задание выдано вашим ученикам', reply_markup=markups.remove_markup())  # TODO add English
        classroom_detail_view(message, task.classroom_id)
    elif message.text in ['❌ Отмена', '❌ Cancel']:
        bot.send_message(message.chat.id, 'Отмена')  # TODO add English
        classroom_detail_view(message, task.classroom_id)
    else:
        task.add(message)
        bot.send_message(message.chat.id, 'Принято')  # TODO add English
        bot.register_next_step_handler(message, compose_task, task)


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@NEW_SUBMISSION/'))
def handle_new_submission_query(call):
    data = get_call_data(call)

    student = Student.get(call.message.chat.id)

    submission = Submission(data['task_id'], student.id, status=SubmissionStatus.DRAFT.value, created_utc=datetime.now(timezone.utc)).save()

    ru_text = "Отправьте мне выполненное задание в любом формате: " \
              "текст, фото, видео, файлы или аудиосообщения; одним или несколькими сообщениями.\n\n" \
              "Когда закончите, просто нажмите кнопку *Отправить на проверку* и я передам его учителю"
    en_text = None
    text = ru_text if student.language_code == 'ru' else en_text

    bot.send_message(call.message.chat.id,
                     text,
                     reply_markup=markups.get_compose_submission_markup(student),
                     parse_mode='Markdown')
    bot.register_next_step_handler(call.message, compose_submission, submission)


def compose_submission(message, submission):
    if message.text in ['Отправить на проверку', 'Submit for review']:
        submission.status = SubmissionStatus.REVIEW.value
        submission.save()
        bot.send_message(message.chat.id, 'Ваше задание отправлено, ждите результата', reply_markup=markups.remove_markup())  # TODO add English
        task_detail_view(message, submission.task_id)
    elif message.text in ['❌ Отмена', '❌ Cancel']:
        bot.send_message(message.chat.id, 'Отмена')  # TODO add English
        task_detail_view(message, submission.task_id)
    else:
        submission.add(message)
        bot.send_message(message.chat.id, 'Принято')  # TODO add English
        bot.register_next_step_handler(message, compose_submission, submission)
