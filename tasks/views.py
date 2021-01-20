from bot import bot
from users.models import Teacher, Student
from tasks.models import STATUS_BADGES
from tasks.markups import get_drawer_markup
from tasks import markups


def task_list_view(user, classroom, message_to_edit=None):
    if message_to_edit:
        bot.edit_message_text(
            f'*{classroom.name}*. {"Список заданий" if user.language_code =="ru" else "Task list"}',
            chat_id=user.id,
            message_id=message_to_edit.message_id,
            reply_markup=markups.get_task_list_inline_markup(user, classroom),
            parse_mode='Markdown')
    else:
        bot.send_message(
            user.id,
            f'*{classroom.name}*',
            reply_markup=markups.get_task_list_inline_markup(user, classroom),
            parse_mode='Markdown')


def task_detail_view(user, task, message_to_edit=None):
    text = f'*{task.name}*' if \
        type(user) is Teacher else f'*{task.name}*. {STATUS_BADGES[user.get_task_status(task.id)][user.language_code]}'

    if message_to_edit:
        bot.edit_message_text(
            text,
            chat_id=user.id,
            message_id=message_to_edit.message_id,
            reply_markup=markups.get_task_detail_inline_markup(user, task),
            parse_mode='Markdown')
    else:
        bot.send_message(
            user.id,
            text,
            reply_markup=markups.get_task_detail_inline_markup(user, task),
            parse_mode='Markdown')


def task_message_list_view(user, task):
    text = f"Содержание задания: *{task.name}*" if user.language_code == 'ru' else f"Content of the task: *{task.name}*"
    bot.send_message(user.id, text, parse_mode='Markdown')
    for task_message in task.messages:
        bot.forward_message(user.id, task_message.teacher_id, task_message.message_id)


def submission_list_view(teacher, task, message_to_edit=None):
    text = f"*{task.name}*. Задания на проверку" if \
        teacher.language_code == 'ru' else f"*{task.name}*. Submissions for review"
    if message_to_edit:
        bot.edit_message_text(
            text,
            chat_id=teacher.id,
            message_id=message_to_edit.message_id,
            reply_markup=markups.get_submissions_for_review_inline_markup(teacher, task),
            parse_mode='Markdown')
    else:
        bot.send_message(
            teacher.id,
            text,
            reply_markup=markups.get_submissions_for_review_inline_markup(teacher, task),
            parse_mode='Markdown')


def submission_message_list_view(user, submission, task):
    student = Student.get(submission.student_id)

    text = f"Выполненное задание: *{task.name}*. Ученик: _{student.fullname}_" if \
        user.language_code == 'ru' else f"Submission: *{task.name}*. Student: _{student.fullname}_"
    bot.send_message(user.id, text, parse_mode='Markdown')

    ru_text = "Нажмите, чтобы исправить ошибки 👇🏻"
    en_text = "Tap to review 👇🏻"
    text = ru_text if user.language_code == 'ru' else en_text

    for submission_message in submission.messages:
        message = bot.forward_message(user.id, submission_message.student_id, submission_message.message_id)
        if type(user) is Teacher and message.photo:
            bot.delete_message(message.chat.id, message.message_id)
            message_with_button = bot.send_photo(
                user.id,
                message.photo[-1].file_id,
            )
            bot.send_message(
                user.id,
                text,
                reply_markup=get_drawer_markup(message.photo[-1].file_id, user,
                                               message_with_button.message_id, submission.id)
            )


def submission_review_result_view(user, submission, task):
    ru_text = f"Задание: *{task.name}*\nОценка: *{submission.assessment}*\n\n" \
              f"Комментарии учителя 👇🏻"
    en_text = f"Task: *{task.name}*\nRate: *{submission.assessment}*\n\n" \
              f"Teacher's comments 👇🏻"
    text = ru_text if user.language_code == 'ru' else en_text
    bot.send_message(user.id, text, parse_mode='Markdown')

    review_messages = submission.review_messages
    if review_messages:
        for review_message in review_messages:
            bot.forward_message(user.id, review_message.teacher_id, message_id=review_message.message_id)
    else:
        bot.send_message(user.id, "Нет комментария" if user.language_code == 'ru' else "No comment")
