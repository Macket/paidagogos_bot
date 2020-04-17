from bot import bot
from users.models import Teacher, Student
from tasks.models import Task
from tasks import markups


def task_detail_view(message, task_id, edit=False):
    user = Teacher.get(message.chat.id) or Student.get(message.chat.id)
    task = Task.get(task_id)

    if edit:
        bot.edit_message_text(
            f'*{task.name}*',
            chat_id=message.chat.id,
            message_id=message.message_id,
            reply_markup=markups.get_task_detail_inline_markup(user, task),
            parse_mode='Markdown')
    else:
        bot.send_message(
            message.chat.id,
            f'*{task.name}*',
            reply_markup=markups.get_task_detail_inline_markup(user, task),
            parse_mode='Markdown')


def task_message_list_view(message, task_id):
    user = Teacher.get(message.chat.id) or Student.get(message.chat.id)
    task = Task.get(task_id)

    text = f"Содержание задания: *{task.name}*" if user.language_code == 'ru' else 'Content of the task: *{task.name}*'
    bot.send_message(message.chat.id, text, parse_mode='Markdown')
    for task_message in task.messages:
        bot.forward_message(message.chat.id, task_message.teacher_id, task_message.message_id)
