from telebot import types
from users.models import Teacher
from tasks.models import STATUS_ICONS


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

    if type(user) is Teacher:
        for task in classroom.tasks:
            count = task.submissions_for_review_count
            count = f"🔔{count}" if count > 0 else ""
            inline_markup.add(
                types.InlineKeyboardButton(
                    text=f"{task.name} ({task.created_utc.strftime('%d.%m.%Y')})  {count}",
                    callback_data='@@TASK/{"task_id": ' + str(task.id) + '}'
                )
            )

        inline_markup.add(
            types.InlineKeyboardButton(
                text="➕ Новое задание" if user.language_code == 'ru' else '➕ New task',
                callback_data='@@NEW_TASK/{"classroom_id": ' + str(classroom.id) + '}'
            )
        )
    else:
        for task in classroom.tasks:
            student = user
            status_icon = STATUS_ICONS[student.get_task_status(task.id)]

            inline_markup.add(
                types.InlineKeyboardButton(
                    text=f"{task.name} ({task.created_utc.strftime('%d.%m.%Y')})  {status_icon}",
                    callback_data='@@TASK/{"task_id": ' + str(task.id) + '}'
                )
            )


    inline_markup.add(
        types.InlineKeyboardButton(
            text="🔙 Назад" if user.language_code == 'ru' else '🔙 Back',
            callback_data='@@CLASSROOMS/{}'
        )
    )

    return inline_markup

