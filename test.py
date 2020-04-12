from telebot import types
from bot import bot
import settings
import requests


def get_drawer_markup(file_id, file_path):

    inline_markup = types.InlineKeyboardMarkup(row_width=1)

    url = f'http://127.0.0.1:5000/drawer/?file_id={file_id}&file_path={file_path}' if settings.DEBUG \
        else f'https://127.0.0.1:5000/drawer/?file_id={file_id}&file_path={file_path}'  # TODO
    inline_markup.add(
        types.InlineKeyboardButton(text='Check', url=url),
    )

    return inline_markup


@bot.message_handler(content_types=['photo'])
def new_photo(message):
    file_info = bot.get_file(message.photo[2].file_id)
    bot.send_message(message.chat.id, 'OK', reply_markup=get_drawer_markup(file_info.file_id, file_info.file_path))
