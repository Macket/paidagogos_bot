import settings
from bot import bot
from users.models import Student
from classrooms.markups import *


def classroom_list_view(user, message_to_edit=None):
    text = '*Классные комнаты*' if user.language_code == 'ru' else '*Classrooms*'
    if message_to_edit:
        bot.edit_message_text(
            text,
            chat_id=user.id,
            message_id=message_to_edit.message_id,
            reply_markup=get_classroom_list_inline_markup(user),
            parse_mode='Markdown')
    else:
        bot.send_message(
            user.id,
            text,
            reply_markup=get_classroom_list_inline_markup(user),
            parse_mode='Markdown')


def classroom_detail_view(user, classroom, message_to_edit=None):
    if message_to_edit:
        bot.edit_message_text(
            f'*{classroom.name}*',
            chat_id=user.id,
            message_id=message_to_edit.message_id,
            reply_markup=get_classroom_detail_inline_markup(user, classroom),
            parse_mode='Markdown')
    else:
        bot.send_message(
            user.id,
            f'*{classroom.name}*',
            reply_markup=get_classroom_detail_inline_markup(user, classroom),
            parse_mode='Markdown')


def classroom_student_list_view(teacher, classroom):
    students = Student.get_classroom_students(classroom.id)
    if len(students) == 0:
        ru_text = "В этой классной комнате пока что нет ни одного ученика"
        en_text = "There are no students in this classroom yet"
        text = ru_text if teacher.language_code == 'ru' else en_text
    else:
        text = f"*{classroom.name}*\n\n"
        for student in students:
            text += f"{student.fullname}\n"

    bot.send_message(teacher.id, text, parse_mode='Markdown')


def classroom_link_view(teacher, classroom):
    ru_text1 = "Вот приглашение в вашу классную комнату 👇🏻 \n\nОтправьте его своим ученикам"
    en_text1 = "Below is an invitation to your classroom 👇🏻 \n\n Send it to your students."
    text1 = ru_text1 if teacher.language_code == 'ru' else en_text1

    bot.send_message(teacher.id, text1)

    ru_text2 = f"Учитель <i>{teacher.fullname}</i> приглашает вас в классную комнату <b>{classroom.name}</b>.\n\n"
    en_text2 = f"Teacher <i>{teacher.fullname}</i> invites you to the classroom <b>{classroom.name}</b>.\n\n"
    text2 = ru_text2 if teacher.language_code == 'ru' else en_text2
    
    bot.send_message(teacher.id, text2, reply_markup=join_classroom_markup(teacher, classroom), parse_mode='HTML')


def classroom_assessments_view(student, classroom):
    assessments = student.get_classroom_assessments(classroom.id)

    text = f"*{classroom.name}*\n\n"
    rate_word = "Оценка" if student.language_code == 'ru' else "Rate"

    if assessments:
        for assessment in assessments:
            text += f"{assessment[0]} _{assessment[1].strftime('%d.%m.%Y')}_\n" \
                    f"{rate_word}: *{assessment[2]}*\n\n"
    else:
        text += "Пока нет ни одной оценки" if student.language_code == 'ru' else "There are no rates yet"
    bot.send_message(student.id, text, parse_mode='Markdown')


def task_assessments_view(teacher, task):
    assessments = teacher.get_task_assessments(task.id)

    text = f"*{task.name}* _{task.created_utc.strftime('%d.%m.%Y')}_\n\n"

    if assessments:
        for assessment in assessments:
            text += f"{assessment[0]}: *{assessment[1]}*\n\n"
    else:
        text += "Пока нет ни одной оценки" if teacher.language_code == 'ru' else "There are no rates yet"
    bot.send_message(teacher.id, text, parse_mode='Markdown')
