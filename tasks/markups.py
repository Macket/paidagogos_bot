from telebot import types


def get_compose_task_markup(teacher):
    ru_markup = types.ReplyKeyboardMarkup()
    ru_markup.add(types.KeyboardButton('Выдать задание'))
    ru_markup.add(types.KeyboardButton('❌ Отмена'))
    en_markup = types.ReplyKeyboardMarkup()
    en_markup.add(types.KeyboardButton('Assign task'))
    en_markup.add(types.KeyboardButton('❌ Cancel'))
    markup = ru_markup if teacher.language_code == 'ru' else en_markup

    return markup


def remove_markup():
    return types.ReplyKeyboardRemove()
