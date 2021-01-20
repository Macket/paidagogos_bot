from bot import bot
from telebot.types import ReplyKeyboardRemove
from classrooms.views import classroom_list_view
from classrooms.markups import are_you_sure_markup


def are_you_sure_request(message, teacher, classroom):
    ru_text = f"Вы уверены, что хотите удалить *{classroom.name}*?"
    en_text = f"Are you sure you want to delete *{classroom.name}*"
    text = ru_text if teacher.language_code == 'ru' else en_text

    bot.send_message(message.chat.id, text, reply_markup=are_you_sure_markup(teacher), parse_mode='Markdown')
    bot.register_next_step_handler(message, are_you_sure_receive, teacher, classroom)


def are_you_sure_receive(message, teacher, classroom):
    if message.text in ["Да", "Yes"]:
        classroom.delete()
        ru_text = f"Классная комната *{classroom.name}* была удалена"
        en_text = f"Classroom *{classroom.name}* has been deleted"
        text = ru_text if teacher.language_code == 'ru' else en_text
    else:
        ru_text = f"Удаление *{classroom.name}* отменено"
        en_text = f"Deletion of * {classroom.name}* is canceled"
        text = ru_text if teacher.language_code == 'ru' else en_text

    bot.send_message(message.chat.id, text, reply_markup=ReplyKeyboardRemove(), parse_mode='Markdown')
    classroom_list_view(teacher)
