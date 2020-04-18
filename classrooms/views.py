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
    url = f'https://t-do.ru/BotoKatalabot?start=slug-{classroom.slug}' if settings.DEBUG \
        else f'https://t-do.ru/paidagogos_bot?start=slug-{classroom.slug}'

    ru_text1 = "Вот приглашение в вашу классную комнату. Отправьте его своим ученикам"
    en_text1 = None  # TODO add English
    text1 = ru_text1 if teacher.language_code == 'ru' else en_text1

    ru_text2 = f"Учитель _{teacher.fullname}_ приглашает вас в классную комнату " \
              f"*{classroom.name}*.\n{url}\n\n" \
              f"Пройдите по ссылке 👆🏻 и нажмите на команду *СТАРТ* (*ЗАПУСТИТЬ*), " \
              f"чтобы в неё войти.\n\n\n" \
              f"_Прежде, чем пройти по ссылке, необходимо установить Telegram_\n" \
              f"*Установить Telegram на Android*: https://play.google.com/store/apps/details?id=org.telegram.messenger\n" \
              f"*Установить Telegram на iOS*: https://apps.apple.com/app/telegram-messenger/id686449807\n" \
              f"*Установить Telegram на Windows*: https://drive.google.com/file/d/1wIZTfi2nXUaPLQlhT-drWKqisiVakSJB/view"
    en_text2 = None
    text2 = ru_text2 if teacher.language_code == 'ru' else en_text2

    bot.send_message(message.chat.id, text1, parse_mode='Markdown')
    bot.send_message(message.chat.id, text2, parse_mode='Markdown')

