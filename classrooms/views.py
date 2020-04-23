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


def classroom_student_list_view(message, classroom_id):
    teacher = Teacher.get(message.chat.id)
    students = Student.get_classroom_students(classroom_id)
    if len(students) == 0:
        ru_text = 'В этой классной комнате пока что нет ни одного ученика'
        en_text = None
        text = ru_text if teacher.language_code == 'ru' else en_text
    else:
        classroom = Classroom.get(classroom_id)
        text = f"*{classroom.name}*\n\n"
        for student in students:
            text += f"{student.fullname}\n"

    bot.send_message(message.chat.id, text, parse_mode='Markdown')


def classroom_link_view(message, classroom_id):
    teacher = Teacher.get(message.chat.id)
    classroom = Classroom.get(classroom_id)
    url_ru = f'https://t-do.ru/BotoKatalabot?start=slug-{classroom.slug}' if settings.DEBUG \
        else f'https://t-do.ru/paidagogos_bot?start=slug-{classroom.slug}'

    url = f'https://t.me/BotoKatalabot?start=slug-{classroom.slug}' if settings.DEBUG \
        else f'https://t.me/paidagogos_bot?start=slug-{classroom.slug}'

    ru_text1 = "Вот приглашение в вашу классную комнату. Отправьте его своим ученикам"
    en_text1 = None  # TODO add English
    text1 = ru_text1 if teacher.language_code == 'ru' else en_text1

    ru_text2 = f"Учитель _{teacher.fullname}_ приглашает вас в классную комнату *{classroom.name}*.\n\n" \
               f"*Ссылка для компьютера*: {url_ru}\n\n" \
               f"*Ссылка для телефона*: {url}\n"
    en_text2 = None
    text2 = ru_text2 if teacher.language_code == 'ru' else en_text2

    bot.send_message(message.chat.id, text1)
    bot.send_message(message.chat.id, text2, parse_mode='Markdown')


def classroom_assessments_view(message, user, classroom):
    if type(user) is Student:
        student = user
        assessments = student.get_classroom_assessments(classroom.id)

        text = f"*{classroom.name}*\n\n"

        for assessment in assessments[:-1]:
            text += f"{assessment}, "
        text += f"{assessments[-1]}"
        bot.send_message(message.chat.id, text, parse_mode='Markdown')
    # TODO add for teachers
