from bot import bot
from users.models import Teacher, Student
from users import markups as user_markups
from classrooms.models import Classroom, ClassroomStudent
from classrooms.views import classroom_list_view
from classrooms.handlers import classroom_name_request
from datetime import datetime, timezone


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
                             reply_markup=user_markups.get_classroom_list_inline_markup(teacher))
        else:
            student = Student.get(message.chat.id) or \
                      Student(message.chat.id, language_code='ru', registered_utc=datetime.now(timezone.utc)).save()
            classroom = Classroom.get_by_slug(classroom_slug)
            teacher = Teacher.get(classroom.teacher_id)
            if not student.check_classroom_student(classroom.id):
                ClassroomStudent(classroom.id, student.id, joined_utc=datetime.now(timezone.utc)).save()  # TODO сделать с нормальной обратной связью, а не всегда писать "Вы добавлены..."
            if not student.fullname:
                student_fullname_request(message)
            else:
                ru_text = f"Вы добавлены в классную комнату: *{classroom.name}*. Учитель: _{teacher.fullname}_"
                en_text = None
                text = ru_text if student.language_code == 'ru' else en_text

                bot.send_message(message.chat.id, text, parse_mode='Markdown')
                bot.send_message(message.chat.id, 'Классные комнаты',
                                 reply_markup=user_markups.get_classroom_list_inline_markup(student))
    else:
        student = Student.get(message.chat.id)
        if student:
            ru_text = "Вы уже зарегистрированы как ученик"
            en_text = None
            text = ru_text if student.language_code == 'ru' else en_text

            bot.send_message(message.chat.id, text)
            bot.send_message(message.chat.id, 'Классные комнаты',
                             reply_markup=user_markups.get_classroom_list_inline_markup(student))
        else:
            # teacher = Teacher(message.chat.id, language_code=message.from_user.language_code)
            Teacher(message.chat.id, language_code='ru', registered_utc=datetime.now(timezone.utc)).save()
            teacher_fullname_request(message)


def teacher_fullname_request(message):
    teacher = Teacher.get(message.chat.id)

    ru_text = f"Введите своё ФИО. Его будут видеть ваши ученики."
    en_text = None
    text = ru_text if teacher.language_code == 'ru' else en_text

    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, teacher_fullname_receive)


def teacher_fullname_receive(message):
    teacher = Teacher.get(message.chat.id)

    teacher.fullname = message.text
    teacher.save()

    classroom_name_request(message)


def student_fullname_request(message):
    student = Student.get(message.chat.id)

    ru_text = "Введите свою фамилию и имя. Их будут видеть ваши учителя."
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

    classroom_list_view(message)
