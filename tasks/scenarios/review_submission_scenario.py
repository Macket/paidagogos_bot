from _datetime import datetime, timezone
from bot import bot
from tasks import markups
from tasks.models import Task, SubmissionReviewMessage, Submission, SubmissionStatus
from tasks.notifications import new_submission_review_result_notification
from tasks.views import task_detail_view
from users.models import Teacher


def submission_comment_request(message, submission_id):
    teacher = Teacher.get(message.chat.id)

    ru_text = "Прокомментируйте задание, отправив любое сообщение"
    en_text = None
    text = ru_text if teacher.language_code == 'ru' else en_text

    bot.send_message(message.chat.id,
                     text,
                     # reply_markup=markups.get_compose_task_markup(teacher),  TODO Добавить клавиатуру
                     parse_mode='Markdown')
    bot.register_next_step_handler(message, submission_comment_receive, submission_id)


def submission_comment_receive(message, submission_id):
    SubmissionReviewMessage(submission_id, message.chat.id, message.message_id,
                            created_utc=datetime.now(timezone.utc)).save()
    submission_assessment_request(message, submission_id)


def submission_assessment_request(message, submission_id):
    teacher = Teacher.get(message.chat.id)

    ru_text = "Поставьте оценку"
    en_text = None
    text = ru_text if teacher.language_code == 'ru' else en_text

    bot.send_message(message.chat.id,
                     text,
                     reply_markup=markups.get_assessment_markup(teacher),
                     parse_mode='Markdown')
    bot.register_next_step_handler(message, submission_assessment_receive, submission_id)


def submission_assessment_receive(message, submission_id):
    teacher = Teacher.get(message.chat.id)
    if len(message.text) > 15:
        ru_text = "Длина оценки не должна превышать 15 символов. Попробуйте ещё раз"
        en_text = None
        text = ru_text if teacher.language_code == 'ru' else en_text
        bot.send_message(message.chat.id,
                         text,
                         reply_markup=markups.get_assessment_markup(teacher),
                         parse_mode='Markdown')
        bot.register_next_step_handler(message, submission_assessment_receive, submission_id)
    else:
        submission = Submission.get(submission_id)
        submission.assessment = message.text
        submission.status = SubmissionStatus.REVIEWED.value
        submission.save()

        ru_text = "Результат проверки отправлен ученику"
        en_text = None
        text = ru_text if teacher.language_code == 'ru' else en_text

        bot.send_message(message.chat.id,
                         text,
                         reply_markup=markups.remove_markup(),
                         parse_mode='Markdown')
        task = Task.get(submission.task_id)
        task_detail_view(teacher, task)
        new_submission_review_result_notification(submission)
