from bot import bot
from users.models import Teacher, Student
from classrooms.models import Classroom
from tasks.models import Task, Submission, STATUS_BADGES
from tasks import markups


def task_list_view(message, classroom_id, edit=False):
    user = Teacher.get(message.chat.id) or Student.get(message.chat.id)
    classroom = Classroom.get(classroom_id)

    if edit:
        bot.edit_message_text(
            f'*{classroom.name}*. {"Список заданий" if user.language_code =="ru" else "Task list"}',
            chat_id=message.chat.id,
            message_id=message.message_id,
            reply_markup=markups.get_task_list_inline_markup(user, classroom),
            parse_mode='Markdown')
    else:
        bot.send_message(
            message.chat.id,
            f'*{classroom.name}*',
            reply_markup=markups.get_task_list_inline_markup(user, classroom),
            parse_mode='Markdown')


# TODO переделать всё view, передав id вместо message
def task_detail_view_(user_id, task_id):
    user = Teacher.get(user_id) or Student.get(user_id)
    task = Task.get(task_id)
    text = f'*{task.name}*' if \
        type(user) is Teacher else f'*{task.name}*. {STATUS_BADGES[user.get_task_status(task.id)]}'

    bot.send_message(
        user_id,
        text,
        reply_markup=markups.get_task_detail_inline_markup(user, task),
        parse_mode='Markdown')


def task_detail_view(message, task_id, edit=False):
    user = Teacher.get(message.chat.id) or Student.get(message.chat.id)
    task = Task.get(task_id)
    text = f'*{task.name}*' if \
        type(user) is Teacher else f'*{task.name}*. {STATUS_BADGES[user.get_task_status(task.id)]}'

    if edit:
        bot.edit_message_text(
            text,
            chat_id=message.chat.id,
            message_id=message.message_id,
            reply_markup=markups.get_task_detail_inline_markup(user, task),
            parse_mode='Markdown')
    else:
        bot.send_message(
            message.chat.id,
            text,
            reply_markup=markups.get_task_detail_inline_markup(user, task),
            parse_mode='Markdown')


def task_message_list_view(message, task_id):
    user = Teacher.get(message.chat.id) or Student.get(message.chat.id)
    task = Task.get(task_id)

    text = f"Содержание задания: *{task.name}*" if user.language_code == 'ru' else 'Content of the task: *{task.name}*'
    bot.send_message(message.chat.id, text, parse_mode='Markdown')
    for task_message in task.messages:
        bot.forward_message(message.chat.id, task_message.teacher_id, task_message.message_id)


# TODO переделать всё view, передав id вместо message
def submission_list_view_(user_id, task_id):
    teacher = Teacher.get(user_id)
    task = Task.get(task_id)

    text = f"*{task.name}*. Задания на проверку" if \
        teacher.language_code == 'ru' else f"*{task.name}*. Submissions for review"

    bot.send_message(
        user_id,
        text,
        reply_markup=markups.get_submissions_for_review_inline_markup(teacher, task),
        parse_mode='Markdown')


# TODO изменить название функции
def submission_list_view(message, task_id, edit):
    teacher = Teacher.get(message.chat.id)
    task = Task.get(task_id)

    text = f"*{task.name}*. Задания на проверку" if \
        teacher.language_code == 'ru' else f"*{task.name}*. Submissions for review"
    if edit:
        bot.edit_message_text(
            text,
            chat_id=message.chat.id,
            message_id=message.message_id,
            reply_markup=markups.get_submissions_for_review_inline_markup(teacher, task),
            parse_mode='Markdown')
    else:
        bot.send_message(
            message.chat.id,
            text,
            reply_markup=markups.get_submissions_for_review_inline_markup(teacher, task),
            parse_mode='Markdown')


def submission_message_list_view(message, submission_id):
    user = Teacher.get(message.chat.id) or Student.get(message.chat.id)
    submission = Submission.get(submission_id)
    task = Task.get(submission.task_id)
    student = Student.get(submission.student_id)

    text = f"Выполненное задание: *{task.name}*. Ученик: _{student.fullname}_" if \
        user.language_code == 'ru' else 'Submission: *{task.name}*. Student: _{student.fullname}_'
    bot.send_message(message.chat.id, text, parse_mode='Markdown')
    for submission_message in submission.messages:
        bot.forward_message(message.chat.id, submission_message.student_id, submission_message.message_id)


def submission_review_result_view_(user_id, submission_id):
    user = Teacher.get(user_id) or Student.get(user_id)
    submission = Submission.get(submission_id)
    task = Task.get(submission.task_id)

    ru_text = f"Задание: *{task.name}*\nОценка: *{submission.assessment}*\n\n" \
              f"Комментарий: _{submission.comment}_"
    en_text = None
    text = ru_text if user.language_code == 'ru' else en_text
    bot.send_message(user_id, text, parse_mode='Markdown')


def submission_review_result_view(message, submission_id):
    user = Teacher.get(message.chat.id) or Student.get(message.chat.id)
    submission = Submission.get(submission_id)
    task = Task.get(submission.task_id)

    ru_text = f"Задание: *{task.name}*\nОценка: *{submission.assessment}*\n\n" \
              f"Комментарий: _{submission.comment}_"
    en_text = None
    text = ru_text if user.language_code == 'ru' else en_text
    bot.send_message(message.chat.id, text, parse_mode='Markdown')
