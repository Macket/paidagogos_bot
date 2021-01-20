import settings
from telebot import types
from users.models import Teacher, Student
from tasks.models import SubmissionStatus
from tasks.models import STATUS_ICONS


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


def get_task_list_inline_markup(user, classroom):
    inline_markup = types.InlineKeyboardMarkup(row_width=1)

    if type(user) is Teacher:
        for task in classroom.tasks:
            count = task.submissions_for_review_count
            count = f"🔔{count}" if count > 0 else ""
            inline_markup.add(
                types.InlineKeyboardButton(
                    text=f"{count} {task.name} ({task.created_utc.strftime('%d.%m.%Y')})",
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
                    text=f"{status_icon} {task.name} ({task.created_utc.strftime('%d.%m.%Y')})",
                    callback_data='@@TASK/{"task_id": ' + str(task.id) + '}'
                )
            )

    inline_markup.add(
        types.InlineKeyboardButton(
            text="🔙 Назад" if user.language_code == 'ru' else '🔙 Back',
            callback_data='@@CLASSROOM/{"classroom_id": ' + str(classroom.id) + '}'
        )
    )

    return inline_markup


def get_task_detail_inline_markup(user, task):
    inline_markup = types.InlineKeyboardMarkup(row_width=1)

    if type(user) is Teacher:
        text_for_review = "На проверку  " if user.language_code == 'ru' else 'Submissions for review  '
        text_for_review += str(task.submissions_for_review_count)
        text_reviewed = "Проверено  " if user.language_code == 'ru' else 'Reviewed submissions  '
        text_reviewed += str(task.submissions_reviewed_count)

        inline_markup.add(
            types.InlineKeyboardButton(
                text=text_for_review,
                callback_data='@@SUBMISSIONS_FOR_REVIEW/{"task_id": ' + str(task.id) + '}'
            ),
            types.InlineKeyboardButton(
                text=text_reviewed,
                callback_data='@@SUBMISSIONS_REVIEWED/{"task_id": ' + str(task.id) + '}'
            ),
            types.InlineKeyboardButton(
                text='Посмотреть задание' if user.language_code == 'ru' else 'View task',
                callback_data='@@TASK_MESSAGES/{"task_id": ' + str(task.id) + '}'
            )
        )
    else:
        student = user
        submission = student.get_submission_for_task(task.id)
        task_status = submission.status if submission else 'NONE'

        if task_status in ['NONE', SubmissionStatus.DRAFT.value]:
            inline_markup.add(
                types.InlineKeyboardButton(
                    text='Посмотреть задание' if user.language_code == 'ru' else 'View task',
                    callback_data='@@TASK_MESSAGES/{"task_id": ' + str(task.id) + '}'
                ),
                types.InlineKeyboardButton(
                    text="Сдать задание" if user.language_code == 'ru' else 'Submit task',
                    callback_data='@@NEW_SUBMISSION/{"task_id": ' + str(task.id) + '}'
                )
            )
        elif task_status == SubmissionStatus.REVIEW.value:
            inline_markup.add(
                types.InlineKeyboardButton(
                    text='Посмотреть задание' if user.language_code == 'ru' else 'View task',
                    callback_data='@@TASK_MESSAGES/{"task_id": ' + str(task.id) + '}'
                ),
                types.InlineKeyboardButton(
                    text="Посмотреть своё выполнение" if user.language_code == 'ru' else 'View my submission',
                    callback_data='@@SUBMISSION_MESSAGES/{"submission_id": ' + str(submission.id) + '}'
                )
            )
        else:
            inline_markup.add(
                types.InlineKeyboardButton(
                    text='Посмотреть задание' if user.language_code == 'ru' else 'View task',
                    callback_data='@@TASK_MESSAGES/{"task_id": ' + str(task.id) + '}'
                ),
                types.InlineKeyboardButton(
                    text="Посмотреть своё выполнение" if user.language_code == 'ru' else 'View my submission',
                    callback_data='@@SUBMISSION_MESSAGES/{"submission_id": ' + str(submission.id) + '}'
                ),
                types.InlineKeyboardButton(
                    text="Посмотреть результат" if user.language_code == 'ru' else 'View result',
                    callback_data='@@SUBMISSION_REVIEW_RESULT/{"submission_id": ' + str(submission.id) + '}'
                )
            )

    inline_markup.add(
        types.InlineKeyboardButton(
            text="🔙 Назад" if user.language_code == 'ru' else '🔙 Back',
            callback_data='@@TASKS/{"classroom_id": ' + str(task.classroom_id) + '}'
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


def get_assessment_markup(teacher):
    ru_markup = types.ReplyKeyboardMarkup(row_width=5)
    ru_markup.add(
        types.KeyboardButton('5'),
        types.KeyboardButton('4'),
        types.KeyboardButton('3'),
        types.KeyboardButton('2'),
        types.KeyboardButton('1'),
    )
    en_markup = types.ReplyKeyboardMarkup(row_width=5)
    en_markup.add(
        types.KeyboardButton('A'),
        types.KeyboardButton('B'),
        types.KeyboardButton('C'),
        types.KeyboardButton('D'),
        types.KeyboardButton('F'),
    )
    markup = ru_markup if teacher.language_code == 'ru' else en_markup

    return markup


def get_drawer_markup(file_id, teacher, message_id=None, submission_id=None):

    url = f'http://127.0.0.1:5000/drawer/?file_id={file_id}&chat_id={teacher.id}' if settings.DEBUG \
        else f'https://paidagogos-drawer.herokuapp.com//drawer/?file_id={file_id}&chat_id={teacher.id}'
    if message_id:
        url += f'&message_id={message_id}'
    if submission_id:
        url += f'&submission_id={submission_id}'

    ru_text = "Исправить ошибки"
    en_text = "Review"
    text = ru_text if teacher.language_code == 'ru' else en_text

    inline_markup = types.InlineKeyboardMarkup(row_width=1)
    inline_markup.add(types.InlineKeyboardButton(text=text, url=url))

    return inline_markup
