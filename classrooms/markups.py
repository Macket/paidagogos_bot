from telebot import types
from users.models import Teacher


def get_teacher_classroom_inline_markup(teacher, classroom):
    inline_markup = types.InlineKeyboardMarkup(row_width=1)

    inline_markup.add(
        types.InlineKeyboardButton(
            text="Задания" if teacher.language_code == 'ru' else 'Tasks',
            callback_data='@@TASKS/{"classroom_id": ' + str(classroom.id) + '}'
        ),
        types.InlineKeyboardButton(
            text="➕ Новое задание" if teacher.language_code == 'ru' else '➕ New task',
            callback_data='@@NEW_TASK/{"classroom_id": ' + str(classroom.id) + '}'
        ),
        types.InlineKeyboardButton(
            text="🔙 Назад" if teacher.language_code == 'ru' else '🔙 Back',
            callback_data='@@CLASSROOMS/{}'
        )
    )

    return inline_markup

