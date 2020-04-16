from telebot import types
from users.models import Teacher


def get_classroom_list_inline_markup(user):
    inline_markup = types.InlineKeyboardMarkup(row_width=1)

    for classroom in user.classrooms:
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
                callback_data="@@NEW_CLASSROOM/{}"
            )
        )

    return inline_markup


def get_classroom_detail_inline_markup(user, classroom):
    inline_markup = types.InlineKeyboardMarkup(row_width=1)

    for task in classroom.tasks:
        inline_markup.add(
            types.InlineKeyboardButton(
                text=f"{task.name} ({task.created_utc.strftime('%d.%m.%Y')})",  # TODO Добавить индикаторы: выполнено/не выполнено
                callback_data='@@TASK/{"task_id": ' + str(task.id) + '}'
            )
        )

    if type(user) is Teacher:
        inline_markup.add(
            types.InlineKeyboardButton(
                text="➕ Новое задание" if user.language_code == 'ru' else '➕ New task',
                callback_data='@@NEW_TASK/{"classroom_id": ' + str(classroom.id) + '}'
            )
        )

    inline_markup.add(
        types.InlineKeyboardButton(
            text="🔙 Назад" if user.language_code == 'ru' else '🔙 Back',
            callback_data='@@CLASSROOMS/{}'
        )
    )

    return inline_markup

