from bot import bot
from users.models import Teacher
from classrooms.models import Classroom
from datetime import datetime, timezone
import settings
from classrooms.views import classroom_detail_view, classroom_list_view
from utils.scripts import get_call_data


@bot.message_handler(commands=['classrooms'])
def handle_classrooms_command(message):
    classroom_list_view(message)


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@CLASSROOMS/'))
def handle_classrooms_query(call):
    classroom_list_view(call.message, edit=True)


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@CLASSROOM/'))
def handle_classroom_query(call):
    data = get_call_data(call)
    classroom_detail_view(call.message, data['classroom_id'], edit=True)


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@NEW_CLASSROOM/'))
def handle_new_classroom_query(call):
    classroom_name_request(call.message)


def classroom_name_request(message):
    teacher = Teacher.get(message.chat.id)

    ru_text = f"Отправьте название класса. Например, «*5А класс. Русский язык*».\n\n" \
              f"Не беспокойтесь об офциальном названии, просто дайте такое имя, " \
              f"которое будет понятно вашим ученикам."
    en_text = None
    text = ru_text if teacher.language_code == 'ru' else en_text

    bot.send_message(message.chat.id, text, parse_mode='Markdown')
    bot.register_next_step_handler(message, classroom_name_receive)


def classroom_name_receive(message):
    teacher = Teacher.get(message.chat.id)
    classroom = Classroom(teacher.id, message.text, created_utc=datetime.now(timezone.utc)).save()

    url = f'https://t.me/BotoKatalabot?start=slug-{classroom.slug}' if settings.DEBUG \
        else f'https://t.me/remote_learning_bot?start=slug-{classroom.slug}'

    ru_text = f"Вот ссылка на вашу классную комнату:\n\n" \
              f"*{classroom.name}*. Учитель: _{teacher.fullname}_\n{url}\n\n" \
              f"Отправьте её своим ученикам. Пройдя по ней и нажав команду *СТАРТ* (*ЗАПУСТИТЬ*), " \
              f"они сразу попадут в вашу классную комнату."
    en_text = None
    text = ru_text if teacher.language_code == 'ru' else en_text

    bot.send_message(message.chat.id, text, parse_mode='Markdown')

    classroom_list_view(message)
