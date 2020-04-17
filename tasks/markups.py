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


def get_task_detail_inline_markup(user, task):
    inline_markup = types.InlineKeyboardMarkup(row_width=1)

    inline_markup.add(
        types.InlineKeyboardButton(
            text='Посмотреть задание' if user.language_code == 'ru' else 'View task',  # TODO Добавить индикаторы: выполнено/не выполнено
            callback_data='@@TASK_MESSAGES/{"task_id": ' + str(task.id) + '}'
        ),
        types.InlineKeyboardButton(
            text="Сдать задание" if user.language_code == 'ru' else 'Submit task',
            callback_data='@@NEW_SUBMISSION/{"task_id": ' + str(task.id) + '}'
        ),
        types.InlineKeyboardButton(
            text="🔙 Назад" if user.language_code == 'ru' else '🔙 Back',
            callback_data='@@CLASSROOM/{"classroom_id": ' + str(task.classroom_id) + '}'
        )
    )

    inline_markup.add(

    )

    return inline_markup
