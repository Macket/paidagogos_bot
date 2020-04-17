from telebot import types
from users.models import Teacher, Student


def get_compose_task_markup(teacher):
    ru_markup = types.ReplyKeyboardMarkup()
    ru_markup.add(types.KeyboardButton('Выдать задание'))
    ru_markup.add(types.KeyboardButton('❌ Отмена'))
    en_markup = types.ReplyKeyboardMarkup()
    en_markup.add(types.KeyboardButton('Assign task'))
    en_markup.add(types.KeyboardButton('❌ Cancel'))
    markup = ru_markup if teacher.language_code == 'ru' else en_markup

    return markup


def get_compose_submission_markup(teacher):
    ru_markup = types.ReplyKeyboardMarkup()
    ru_markup.add(types.KeyboardButton('Отправить на проверку'))
    ru_markup.add(types.KeyboardButton('❌ Отмена'))
    en_markup = types.ReplyKeyboardMarkup()
    en_markup.add(types.KeyboardButton('Submit for review'))
    en_markup.add(types.KeyboardButton('❌ Cancel'))
    markup = ru_markup if teacher.language_code == 'ru' else en_markup

    return markup


def remove_markup():
    return types.ReplyKeyboardRemove()


def get_task_detail_inline_markup(user, task):
    inline_markup = types.InlineKeyboardMarkup(row_width=1)

    if type(user) is Teacher:
        inline_markup.add(
            types.InlineKeyboardButton(
                text="На проверку" if user.language_code == 'ru' else 'Submissions for review',
                callback_data='@@SUBMISSIONS_FOR_REVIEW/{"task_id": ' + str(task.id) + '}'
            ),
            types.InlineKeyboardButton(
                text="Проверено" if user.language_code == 'ru' else 'Reviewed submissions',
                callback_data='@@SUBMISSIONS_REVIEWED/{"task_id": ' + str(task.id) + '}'
            ),
            types.InlineKeyboardButton(
                text='Посмотреть задание' if user.language_code == 'ru' else 'View task',
                # TODO Добавить индикаторы: выполнено/не выполнено
                callback_data='@@TASK_MESSAGES/{"task_id": ' + str(task.id) + '}'
            )
        )
    else:
        inline_markup.add(
            types.InlineKeyboardButton(
                text='Посмотреть задание' if user.language_code == 'ru' else 'View task',
                # TODO Добавить индикаторы: выполнено/не выполнено
                callback_data='@@TASK_MESSAGES/{"task_id": ' + str(task.id) + '}'
            ),
            types.InlineKeyboardButton(
                text="Сдать задание" if user.language_code == 'ru' else 'Submit task',
                callback_data='@@NEW_SUBMISSION/{"task_id": ' + str(task.id) + '}'
            )
        )

    inline_markup.add(
        types.InlineKeyboardButton(
            text="🔙 Назад" if user.language_code == 'ru' else '🔙 Back',
            callback_data='@@CLASSROOM/{"classroom_id": ' + str(task.classroom_id) + '}'
        )
    )

    return inline_markup


def get_submissions_for_review_inline_markup(teacher, task):
    inline_markup = types.InlineKeyboardMarkup(row_width=1)

    for submission in task.submissions_for_review:
        student = Student.get(submission.student_id)
        inline_markup.add(
            types.InlineKeyboardButton(
                text=f"{student.fullname} ({submission.created_utc.strftime('%d.%m.%Y')})",
                callback_data='@@SUBMISSION_REVIEW/{"submission_id": ' + str(submission.id) + '}'
            )
        )

    inline_markup.add(
        types.InlineKeyboardButton(
            text="🔙 Назад" if teacher.language_code == 'ru' else '🔙 Back',
            callback_data='@@TASK/{"task_id": ' + str(task.id) + '}'
        )
    )

    return inline_markup
