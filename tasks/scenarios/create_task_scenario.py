from _datetime import datetime, timezone
from bot import bot
from classrooms.models import Classroom
from classrooms.views import classroom_detail_view
from tasks import markups
from tasks.models import Task
from tasks.notifications import new_task_notification
from users.models import Teacher


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
    teacher = Teacher.get(message.chat.id)
    if message.text in ['Выдать задание', 'Assign task']:
        bot.send_message(message.chat.id, 'Задание выдано вашим ученикам', reply_markup=markups.remove_markup())  # TODO add English

        classroom = Classroom.get(task.classroom_id)
        classroom_detail_view(teacher, classroom)

        new_task_notification(task)
    elif message.text in ['❌ Отмена', '❌ Cancel']:
        bot.send_message(message.chat.id, 'Отмена', reply_markup=markups.remove_markup())  # TODO add English

        classroom = Classroom.get(task.classroom_id)
        classroom_detail_view(teacher, classroom)
        task.delete()
    else:
        task.add(message)
        bot.send_message(
            message.chat.id,
            'Отправьте ещё что-то или нажмите *Выдать задание*',
            reply_markup=markups.get_compose_task_markup(teacher),
            parse_mode='Markdown',
        )  # TODO add English
        bot.register_next_step_handler(message, compose_task, task)
