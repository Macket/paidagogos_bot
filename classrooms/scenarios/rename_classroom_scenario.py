from bot import bot
from classrooms.views import classroom_detail_view
from users.models import Teacher


def classroom_name_request(message, teacher, classroom):
    ru_text = f"Отправьте новое название класса"
    en_text = None
    text = ru_text if teacher.language_code == 'ru' else en_text

    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, classroom_name_receive, classroom)


def classroom_name_receive(message, classroom):
    teacher = Teacher.get(message.chat.id)
    classroom.name = message.text
    classroom.save()
    classroom_detail_view(teacher, classroom, message_to_edit=message)
