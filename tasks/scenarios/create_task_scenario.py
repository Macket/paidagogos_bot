from _datetime import datetime, timezone
from bot import bot
from classrooms.models import Classroom
from classrooms.views import classroom_detail_view
from tasks import markups
from utils.markups import remove_markup
from tasks.models import Task
from tasks.notifications import new_task_notification
from users.models import Teacher


def task_name_request(message, classroom_id):
    teacher = Teacher.get(message.chat.id)

    ru_text = "Отправьте название задания"
    en_text = "Send the name of the task"
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
    en_text = "Send me the task in any format: " \
              "text, photo, video, files or audio messages; one or more messages."
    text = ru_text if teacher.language_code == 'ru' else en_text

    bot.send_message(message.chat.id,
                     text,
                     parse_mode='Markdown')
    bot.register_next_step_handler(message, compose_task, task)


def compose_task(message, task):
    teacher = Teacher.get(message.chat.id)
    if message.text in ['Выдать задание', 'Assign task']:
        ru_text = "Задание выдано вашим ученикам"
        en_text = "The task has been sent to your students"
        text = ru_text if teacher.language_code == 'ru' else en_text

        bot.send_message(message.chat.id, text, reply_markup=remove_markup())

        classroom = Classroom.get(task.classroom_id)
        classroom_detail_view(teacher, classroom)

        new_task_notification(task)
    elif message.text in ['❌ Отмена', '❌ Cancel']:
        ru_text = "Отмена"
        en_text = "Cancel"
        text = ru_text if teacher.language_code == 'ru' else en_text

        bot.send_message(message.chat.id, text, reply_markup=remove_markup())

        classroom = Classroom.get(task.classroom_id)
        classroom_detail_view(teacher, classroom)
        task.delete()
    else:
        task.add(message)

        ru_text = "Отправьте ещё что-то или нажмите *Выдать задание*"
        en_text = "Send something else or tap *Assign task*"
        text = ru_text if teacher.language_code == 'ru' else en_text

        bot.send_message(
            message.chat.id,
            text,
            reply_markup=markups.get_compose_task_markup(teacher),
            parse_mode='Markdown',
        )
        bot.register_next_step_handler(message, compose_task, task)
