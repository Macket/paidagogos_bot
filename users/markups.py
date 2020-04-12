from telebot import types
# from users.data import preparing_habits
from users.models import User
# import settings


def get_role_markup(user_id):
    user = User.get(user_id)
    ru_markup = types.ReplyKeyboardMarkup(row_width=1)
    ru_markup.add(
        types.KeyboardButton('Ученик'),
        types.KeyboardButton('Учитель'),
    )
    en_markup = types.ReplyKeyboardMarkup(row_width=1)
    en_markup.add(
        types.KeyboardButton('Student'),
        types.KeyboardButton('Teacher'),
    )
    markup = ru_markup if user.language_code == 'ru' else en_markup

    return markup


# def get_cancel_markup(user_id):
#     user = User.get(user_id)
#     ru_markup = types.ReplyKeyboardMarkup()
#     ru_markup.add(types.KeyboardButton('❌ Отмена'))
#     en_markup = types.ReplyKeyboardMarkup()
#     en_markup.add(types.KeyboardButton('❌ Cancel'))
#     markup = ru_markup if user.language_code == 'ru' else en_markup
#
#     return markup
#
#
# def get_habits_markup(user_id):
#     user = User.get(user_id)
#
#     ru_markup = types.ReplyKeyboardMarkup(row_width=1)
#     ru_markup.add(
#         types.KeyboardButton('Бросить курить'),
#         types.KeyboardButton('Не тратить время на YouTube'),
#         types.KeyboardButton('Регулярно заниматься спортом'),
#         types.KeyboardButton('Не зависать в Instagram'),
#         types.KeyboardButton('Просыпаться раньше'),
#         types.KeyboardButton('Регулярно читать книги'),
#         types.KeyboardButton('Сбросить вес'),
#         types.KeyboardButton('Другое...'),
#     )
#     en_markup = types.ReplyKeyboardMarkup(row_width=1)
#     en_markup.add(
#         types.KeyboardButton('Quit smoking'),
#         types.KeyboardButton("Don't waste time on YouTube"),
#         types.KeyboardButton('Exercise regularly'),
#         types.KeyboardButton('Wake up earlier'),
#         types.KeyboardButton('Lose weight'),
#         types.KeyboardButton('Read books regularly'),
#         types.KeyboardButton('Other...'),
#     )
#     markup = ru_markup if user.language_code == 'ru' else en_markup
#
#     return markup
#
#
# def get_languages_markup():
#     markup = types.ReplyKeyboardMarkup(row_width=2)
#     markup.add(
#         types.KeyboardButton('🇷🇺Русский'),
#         types.KeyboardButton('🇬🇧English'))
#     return markup
