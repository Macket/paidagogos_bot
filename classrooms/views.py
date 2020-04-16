from bot import bot
from users.models import Teacher, Student
from classrooms.models import Classroom
from classrooms import markups


def classroom_list_view(message, edit=False):
    user = Teacher.get(message.chat.id) or Student.get(message.chat.id)
    if edit:
        bot.edit_message_text(
            '*Классные комнаты*',
            chat_id=message.chat.id,
            message_id=message.message_id,
            reply_markup=markups.get_classroom_list_inline_markup(user),
            parse_mode='Markdown')
    else:
        bot.send_message(
            message.chat.id,
            '*Классные комнаты*',
            reply_markup=markups.get_classroom_list_inline_markup(user),
            parse_mode='Markdown')


def classroom_detail_view(message, classroom_id, edit=False):
    user = Teacher.get(message.chat.id) or Student.get(message.chat.id)
    classroom = Classroom.get(classroom_id)

    if edit:
        bot.edit_message_text(
            f'*{classroom.name}*',
            chat_id=message.chat.id,
            message_id=message.message_id,
            reply_markup=markups.get_classroom_detail_inline_markup(user, classroom),
            parse_mode='Markdown')
    else:
        bot.send_message(
            message.chat.id,
            f'*{classroom.name}*',
            reply_markup=markups.get_classroom_detail_inline_markup(user, classroom),
            parse_mode='Markdown')
