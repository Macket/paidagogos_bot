from datetime import datetime, timezone
from bot import bot
from users.models import Teacher
from classrooms.models import Classroom
from classrooms.views import classroom_link_view, classroom_list_view


def classroom_name_request(message):
    teacher = Teacher.get(message.chat.id)

    ru_text = f"Отправьте название класса"
    en_text = None
    text = ru_text if teacher.language_code == 'ru' else en_text

    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, classroom_name_receive)


def classroom_name_receive(message):
    teacher = Teacher.get(message.chat.id)
    classroom = Classroom(teacher.id, message.text, created_utc=datetime.now(timezone.utc)).save()

    classroom_link_view(message, classroom.id)
    classroom_list_view(teacher)
