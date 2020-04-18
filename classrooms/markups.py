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
        inline_markup.add(
            types.InlineKeyboardButton(
                text="Задания" if user.language_code == 'ru' else 'Tasks',
                callback_data='@@TASKS/{"classroom_id": ' + str(classroom.id) + '}'
            ),
            types.InlineKeyboardButton(
                text="Ссылка для учеников" if user.language_code == 'ru' else 'Link for students',
                callback_data='@@CLASSROOM_LINK/{"classroom_id": ' + str(classroom.id) + '}'
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

