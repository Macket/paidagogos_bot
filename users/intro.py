# from telebot import types
from bot import bot
from users.models import User, Student
from classrooms.models import Classroom
import settings
# from datetime import datetime
# from tzwhere import tzwhere
# import re
# import pytz
import users.markups as markups
# from users.utils import get_schedule, get_user_naming
# from checks.models import Check
# from habits.models import Habit
# from users.data import preparing_habits
from users.roles import Roles


@bot.message_handler(commands=['start'])
def role_request(message):
    classroom_slug = message.text[12:] if message.text[7:] else None
    if classroom_slug:
        classroom = Classroom.get_by_slug(classroom_slug)
        student = Student(message.chat.id, classroom.id, language_code='en')
        student.save()
        student_fullname_request(message)
    else:
        # user = User(message.chat.id, language_code=message.from_user.language_code)
        user = User(message.chat.id, language_code='en', role=Roles.TEACHER.value)
        user.save()
        fullname_request(message)


def fullname_request(message):
    print('REQUEST')
    user = User.get(message.chat.id)

    ru_text = f''
    en_text = f"What is your full name?"
    text = ru_text if user.language_code == 'ru' else en_text

    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, fullname_receive)


def fullname_receive(message):
    user = User.get(message.chat.id)

    user.fullname = message.text
    user.save()

    classroom_request(message)


# def role_request(message):
#     user = User.get(message.chat.id)
#
#     ru_text = f""
#     en_text = f"Choose your role"
#     text = ru_text if user.language_code == 'ru' else en_text
#
#     bot.send_message(message.chat.id, text, reply_markup=markups.get_role_markup(message.chat.id))
#     bot.register_next_step_handler(message, role_receive)
#
#
# def role_receive(message):
#     user = User.get(message.chat.id)
#
#     user.f = Roles.TEACHER.value if message.text in ['Student', 'Учитель'] else Roles.STUDENT.value
#     user.save()
#
#     classroom_request(message)


def classroom_request(message):
    user = User.get(message.chat.id)

    ru_text = f""
    en_text = f"Write your classroom name. Don't worry about " \
              f"its official name. Just enter a name that students will understand."
    text = ru_text if user.language_code == 'ru' else en_text

    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, classroom_receive)


def classroom_receive(message):
    user = User.get(message.chat.id)

    classroom = Classroom(user.id, message.text).save()

    url = f'https://t.me/BotoKatalabot?start=slug_{classroom.slug}' if settings.DEBUG \
        else f'https://t.me/remote_learning_bot?start=slug_{classroom.slug}'

    ru_text = f""
    en_text = f"Here is your classroom link: {url}\n\n Share it with your students"
    text = ru_text if user.language_code == 'ru' else en_text

    bot.send_message(message.chat.id, text)


def student_fullname_request(message):
    student = Student.get(message.chat.id)

    ru_text = f''
    en_text = f"What is your full name?"
    text = ru_text if student.language_code == 'ru' else en_text

    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, student_fullname_receive)


def student_fullname_receive(message):
    student = Student.get(message.chat.id)

    student.fullname = message.text
    student.save()

    ru_text = f''
    en_text = f"Send me photos of your homework, I'll forward them to your teacher and come back with feedback"
    text = ru_text if student.language_code == 'ru' else en_text

    bot.send_message(message.chat.id, text)
