import settings
from bot import bot
from users.models import Teacher, Student
from classrooms.models import Classroom
from classrooms import markups


def classroom_list_view(message, edit=False):
    user = Teacher.get(message.chat.id) or Student.get(message.chat.id)
    text = '*Классные комнаты*' if user.language_code == 'ru' else '*Classrooms*'
    if edit:
        bot.edit_message_text(
            text,
            chat_id=message.chat.id,
            message_id=message.message_id,
            reply_markup=markups.get_classroom_list_inline_markup(user),
            parse_mode='Markdown')
    else:
        bot.send_message(
            message.chat.id,
            text,
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


def classroom_link_view(message, classroom_id):
    teacher = Teacher.get(message.chat.id)
    classroom = Classroom.get(classroom_id)
    url = f'https://t.me/BotoKatalabot?start=slug-{classroom.slug}' if settings.DEBUG \
        else f'https://t.me/remote_learning_bot?start=slug-{classroom.slug}'

    ru_text = f"Вот ссылка на вашу классную комнату:\n\n" \
              f"*{classroom.name}*. Учитель: _{teacher.fullname}_\n{url}\n\n" \
              f"Отправьте её своим ученикам. Пройдя по ней и нажав команду *СТАРТ* (*ЗАПУСТИТЬ*), " \
              f"они сразу попадут в вашу классную комнату."
    en_text = None
    text = ru_text if teacher.language_code == 'ru' else en_text

    bot.send_message(message.chat.id, text, parse_mode='Markdown')
