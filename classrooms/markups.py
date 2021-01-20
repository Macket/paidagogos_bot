from telebot import types
import settings
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

    if type(user) is Teacher:
        inline_markup.add(
            types.InlineKeyboardButton(
                text="Задания" if user.language_code == 'ru' else 'Tasks',
                callback_data='@@TASKS/{"classroom_id": ' + str(classroom.id) + '}'
            ),
            types.InlineKeyboardButton(
                text="Список учеников" if user.language_code == 'ru' else 'Students',
                callback_data='@@CLASSROOM_STUDENTS/{"classroom_id": ' + str(classroom.id) + '}'
            ),
            types.InlineKeyboardButton(
                text="Ссылка для учеников" if user.language_code == 'ru' else 'Link for students',
                callback_data='@@CLASSROOM_LINK/{"classroom_id": ' + str(classroom.id) + '}'
            ),
            types.InlineKeyboardButton(
                text="Переименовать классную комнату" if user.language_code == 'ru' else 'Rename classroom',
                callback_data='@@CLASSROOM_RENAME/{"classroom_id": ' + str(classroom.id) + '}'
            ),
            types.InlineKeyboardButton(
                text="🗑 Удалить классную комнату" if user.language_code == 'ru' else '🗑 Delete classroom',
                callback_data='@@CLASSROOM_DELETE/{"classroom_id": ' + str(classroom.id) + '}'
            )
        )
    else:
        inline_markup.add(
            types.InlineKeyboardButton(
                text="Задания" if user.language_code == 'ru' else 'Tasks',
                callback_data='@@TASKS/{"classroom_id": ' + str(classroom.id) + '}'
            ),
            types.InlineKeyboardButton(
                text="Мои оценки" if user.language_code == 'ru' else 'My grades',
                callback_data='@@CLASSROOM_ASSESSMENTS/{"classroom_id": ' + str(classroom.id) + '}'
            ),
        )

    inline_markup.add(
        types.InlineKeyboardButton(
            text="🔙 Назад" if user.language_code == 'ru' else '🔙 Back',
            callback_data='@@CLASSROOMS/{}'
        )
    )

    return inline_markup


def are_you_sure_markup(teacher):
    ru_markup = types.ReplyKeyboardMarkup(row_width=2)
    ru_markup.add(types.KeyboardButton('Да'))
    ru_markup.add(types.KeyboardButton('Нет'))
    en_markup = types.ReplyKeyboardMarkup(row_width=2)
    en_markup.add(types.KeyboardButton('Yes'))
    en_markup.add(types.KeyboardButton('No'))
    markup = ru_markup if teacher.language_code == 'ru' else en_markup

    return markup


def join_classroom_markup(teacher, classroom):
    url = f'https://t.me/remote_learning_bot?start=slug-{classroom.slug}' if settings.DEBUG \
        else f'https://t.me/paidagogos_bot?start=slug-{classroom.slug}'

    ru_text = "Присоединиться"
    en_text = "Join"
    text = ru_text if teacher.language_code == 'ru' else en_text

    inline_markup = types.InlineKeyboardMarkup(row_width=1)
    inline_markup.add(types.InlineKeyboardButton(text=text, url=url))

    return inline_markup
