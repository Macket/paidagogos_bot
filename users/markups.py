from telebot import types
from users.models import Teacher


def get_classroom_list_inline_markup(user):
    inline_markup = types.InlineKeyboardMarkup(row_width=1)

    for classroom in user.get_classrooms():
        inline_markup.add(
            types.InlineKeyboardButton(
                text=classroom.name if type(user) is Teacher else
                f"{classroom.name} ({Teacher.get(classroom.teacher_id).fullname})",
                callback_data='@@CLASSROOM/{"classroom_id": ' + str(classroom.id) + '}'
            )
        )

    if type(user) is Teacher:
        inline_markup.add(
            types.InlineKeyboardButton(
                text=f"🆕 {'Новый класс' if user.language_code == 'ru' else 'New class'}",
                callback_data="@@NEW_CLASS/{}"
            )
        )

    return inline_markup
