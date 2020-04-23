from bot import bot
from users.models import Teacher, Student
from tasks.models import Task, Submission, SubmissionStatus
from tasks import markups
from datetime import datetime, timezone
from classrooms.views import classroom_detail_view
from tasks.views import task_list_view, task_detail_view, task_message_list_view, \
    submission_list_view, submission_message_list_view, submission_review_result_view
from tasks.notifications import new_task_notification, new_submission_review_result_notification
from utils.scripts import get_call_data


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@TASKS/'))
def handle_task_query(call):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    data = get_call_data(call)
    task_list_view(call.message, data['classroom_id'], edit=True)


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@TASK/'))
def handle_task_query(call):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    data = get_call_data(call)
    task_detail_view(call.message, data['task_id'], edit=True)


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@TASK_MESSAGES/'))
def handle_task_messages_query(call):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    data = get_call_data(call)
    task_message_list_view(call.message, data['task_id'])
    task_detail_view(call.message, data['task_id'])


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@NEW_TASK/'))
def handle_new_task_query(call):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    data = get_call_data(call)
    task_name_request(call.message, data['classroom_id'])


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@SUBMISSIONS_FOR_REVIEW/'))
def handle_submissions_for_review_query(call):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    data = get_call_data(call)
    submission_list_view(call.message, data['task_id'], edit=True)


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@SUBMISSION_MESSAGES/'))
def handle_submission_message_list_query(call):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    data = get_call_data(call)
    submission_message_list_view(call.message, data['submission_id'])
    submission = Submission.get(data['submission_id'])
    task_detail_view(call.message, submission.task_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@SUBMISSION_REVIEW/'))
def handle_submission_review_query(call):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    data = get_call_data(call)
    submission_message_list_view(call.message, data['submission_id'])
    submission_comment_request(call.message, data['submission_id'])


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@SUBMISSION_REVIEW_RESULT/'))
def handle_submission_review_result_query(call):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    data = get_call_data(call)
    submission_review_result_view(call.message, data['submission_id'])
    submission = Submission.get(data['submission_id'])
    task = Task.get(submission.task_id)
    classroom_detail_view(call.message, task.classroom_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@NEW_SUBMISSION/'))
def handle_new_submission_query(call):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    data = get_call_data(call)

    student = Student.get(call.message.chat.id)

    submission = Submission(data['task_id'], student.id, status=SubmissionStatus.DRAFT.value, created_utc=datetime.now(timezone.utc)).save()

    ru_text = "Отправьте мне выполненное задание в любом формате: " \
              "текст, фото, видео, файлы или аудиосообщения; одним или несколькими сообщениями."
    en_text = None
    text = ru_text if student.language_code == 'ru' else en_text

    bot.send_message(call.message.chat.id,
                     text,
                     parse_mode='Markdown')
    bot.register_next_step_handler(call.message, compose_submission, submission)


def task_name_request(message, classroom_id):
    teacher = Teacher.get(message.chat.id)

    ru_text = "Отправьте название задания"
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
              "текст, фото, видео, файлы или аудиосообщения; одним или несколькими сообщениями."
    en_text = None
    text = ru_text if teacher.language_code == 'ru' else en_text

    bot.send_message(message.chat.id,
                     text,
                     parse_mode='Markdown')
    bot.register_next_step_handler(message, compose_task, task)


def compose_task(message, task):
    if message.text in ['Выдать задание', 'Assign task']:
        bot.send_message(message.chat.id, 'Задание выдано вашим ученикам', reply_markup=markups.remove_markup())  # TODO add English
        classroom_detail_view(message, task.classroom_id)
        new_task_notification(task)
    elif message.text in ['❌ Отмена', '❌ Cancel']:
        bot.send_message(message.chat.id, 'Отмена', reply_markup=markups.remove_markup())  # TODO add English
        classroom_detail_view(message, task.classroom_id)
        task.delete()
    else:
        teacher = Teacher.get(message.chat.id)
        task.add(message)
        bot.send_message(
            message.chat.id,
            'Отправьте ещё что-то или нажмите *Выдать задание*',
            reply_markup=markups.get_compose_task_markup(teacher),
            parse_mode='Markdown',
        )  # TODO add English
        bot.register_next_step_handler(message, compose_task, task)


def compose_submission(message, submission):
    if message.text in ['Отправить на проверку', 'Submit for review']:
        submission.status = SubmissionStatus.REVIEW.value
        submission.save()
        bot.send_message(message.chat.id, 'Ваше задание отправлено, ждите результата', reply_markup=markups.remove_markup())  # TODO add English
        task_detail_view(message, submission.task_id)
    elif message.text in ['❌ Отмена', '❌ Cancel']:
        bot.send_message(message.chat.id, 'Отмена', reply_markup=markups.remove_markup())  # TODO add English
        task_detail_view(message, submission.task_id)
        submission.delete()
    else:
        student = Student.get(message.chat.id)
        submission.add(message)
        bot.send_message(
            message.chat.id,
            'Отправьте ещё что-то или нажмите *Отправить на проверку*',
            reply_markup=markups.get_compose_submission_markup(student),
            parse_mode='Markdown',
        )  # TODO add English
        bot.register_next_step_handler(message, compose_submission, submission)


def submission_comment_request(message, submission_id):
    teacher = Teacher.get(message.chat.id)

    ru_text = "Прокомментируйте задание, отправив текстовое сообщение (не более 1000 символов)"
    en_text = None
    text = ru_text if teacher.language_code == 'ru' else en_text

    bot.send_message(message.chat.id,
                     text,
                     # reply_markup=markups.get_compose_task_markup(teacher),  TODO Добавить клавиатуру
                     parse_mode='Markdown')
    bot.register_next_step_handler(message, submission_comment_receive, submission_id)


def submission_comment_receive(message, submission_id):
    submission = Submission.get(submission_id)
    submission.comment = message.text
    submission.save()
    submission_assessment_request(message, submission_id)


def submission_assessment_request(message, submission_id):
    teacher = Teacher.get(message.chat.id)

    ru_text = "Поставьте оценку"
    en_text = None
    text = ru_text if teacher.language_code == 'ru' else en_text

    bot.send_message(message.chat.id,
                     text,
                     reply_markup=markups.get_assessment_markup(teacher),
                     parse_mode='Markdown')
    bot.register_next_step_handler(message, submission_assessment_receive, submission_id)


def submission_assessment_receive(message, submission_id):
    teacher = Teacher.get(message.chat.id)
    submission = Submission.get(submission_id)
    submission.assessment = message.text
    submission.status = SubmissionStatus.REVIEWED.value
    submission.save()

    ru_text = "Результат проверки отправлен ученику"
    en_text = None
    text = ru_text if teacher.language_code == 'ru' else en_text

    bot.send_message(message.chat.id,
                     text,
                     reply_markup=markups.remove_markup(),
                     parse_mode='Markdown')
    task_detail_view(message, submission.task_id)
    new_submission_review_result_notification(submission)
