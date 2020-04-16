# from telebot import types
from bot import bot
from users.models import Teacher, Student
from users import markups as user_markups
from classrooms.models import Classroom, ClassroomStudent
from datetime import datetime, timezone
import settings


@bot.message_handler(commands=['start'])
def start(message):
    classroom_slug = message.text[12:] if message.text[7:] else None
    if classroom_slug:
        teacher = Teacher.get(message.chat.id)
        if teacher:
            ru_text = "Вы уже зарегистрированы как учитель и не можете добавляться в классы"
            en_text = None
            text = ru_text if teacher.language_code == 'ru' else en_text

            bot.send_message(message.chat.id, text)
            bot.send_message(message.chat.id, "Классные комнаты",
                             reply_markup=user_markups.get_classrooms_inline_markup(teacher))
        else:
            student = Student.get(message.chat.id) or \
                      Student(message.chat.id, language_code='ru', registered_utc=datetime.now(timezone.utc)).save()
            classroom = Classroom.get_by_slug(classroom_slug)
            teacher = Teacher.get(classroom.teacher_id)
            ClassroomStudent(classroom.id, student.id, joined_utc=datetime.now(timezone.utc)).save()  # TODO исключить дублирование
            if not student.fullname:
                student_fullname_request(message)
            else:
                ru_text = f"Вы добавлены в классную комнату: *{classroom.name}*. Учитель: _{teacher.fullname}_"
                en_text = None
                text = ru_text if student.language_code == 'ru' else en_text

                bot.send_message(message.chat.id, text, parse_mode='Markdown')
                bot.send_message(message.chat.id, 'Классные комнаты',
                                 reply_markup=user_markups.get_classrooms_inline_markup(student))
    else:
        student = Student.get(message.chat.id)
        if student:
            ru_text = "Вы уже зарегистрированы как ученик"
            en_text = None
            text = ru_text if student.language_code == 'ru' else en_text

            bot.send_message(message.chat.id, text)
            bot.send_message(message.chat.id, 'Классные комнаты',
                             reply_markup=user_markups.get_classrooms_inline_markup(student))
        else:
            # teacher = Teacher(message.chat.id, language_code=message.from_user.language_code)
            Teacher(message.chat.id, language_code='ru', registered_utc=datetime.now(timezone.utc)).save()
            teacher_fullname_request(message)


def teacher_fullname_request(message):
    teacher = Teacher.get(message.chat.id)

    ru_text = f"Введите своё полное имя. Его будут видеть ваши ученики."
    en_text = None
    text = ru_text if teacher.language_code == 'ru' else en_text

    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, teacher_fullname_receive)


def teacher_fullname_receive(message):
    teacher = Teacher.get(message.chat.id)

    teacher.fullname = message.text
    teacher.save()

    classroom_request(message)


def classroom_request(message):
    teacher = Teacher.get(message.chat.id)

    ru_text = f"Отправьте название класса. Например, «*7Б класс. Математика*».\n\n" \
              f"Не беспокойтесь об офциальном названии, просто дайте такое имя, " \
              f"которое будет понятно вашим ученикам."
    en_text = None
    text = ru_text if teacher.language_code == 'ru' else en_text

    bot.send_message(message.chat.id, text, parse_mode='Markdown')
    bot.register_next_step_handler(message, classroom_receive)


def classroom_receive(message):
    teacher = Teacher.get(message.chat.id)
    classroom = Classroom(teacher.id, message.text, created_utc=datetime.now(timezone.utc)).save()

    url = f'https://t.me/BotoKatalabot?start=slug-{classroom.slug}' if settings.DEBUG \
        else f'https://t.me/remote_learning_bot?start=slug-{classroom.slug}'

    ru_text = f"Вот ссылка на вашу классную комнату:\n\n" \
              f"*{classroom.name}*. Учитель: _{teacher.fullname}_\n{url}\n\n" \
              f"Отправьте её своим ученикам. Пройдя по ней и нажав команду *ЗАПУСТИТЬ*, " \
              f"они сразу попадут в вашу классную комнату."
    en_text = None
    text = ru_text if teacher.language_code == 'ru' else en_text

    bot.send_message(message.chat.id, text, parse_mode='Markdown')
    bot.send_message(message.chat.id, "Классные комнаты",
                     reply_markup=user_markups.get_classrooms_inline_markup(teacher))


def student_fullname_request(message):
    student = Student.get(message.chat.id)

    ru_text = "Введите своё полное имя. Его будут видеть ваши учителя."
    en_text = None
    text = ru_text if student.language_code == 'ru' else en_text

    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, student_fullname_receive)


def student_fullname_receive(message):
    student = Student.get(message.chat.id)

    student.fullname = message.text
    student.save()

    classroom = student.get_classrooms()[-1]
    teacher = Teacher.get(classroom.teacher_id)

    ru_text = f"Вы добавлены в классную комнату: *{classroom.name}*. Учитель: _{teacher.fullname}_"
    en_text = None
    text = ru_text if student.language_code == 'ru' else en_text

    bot.send_message(message.chat.id, text, parse_mode='Markdown')
    bot.send_message(message.chat.id, 'Классные комнаты',
                     reply_markup=user_markups.get_classrooms_inline_markup(student))
