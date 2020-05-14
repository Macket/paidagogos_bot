from bot import bot
from tasks import markups
from utils.markups import remove_markup
from tasks.models import Task, SubmissionStatus
from tasks.views import task_detail_view
from users.models import Student


def compose_submission(message, submission):
    student = Student.get(message.chat.id)

    if message.text in ['Отправить на проверку', 'Submit for review']:
        submission.status = SubmissionStatus.REVIEW.value
        submission.save()
        bot.send_message(
            message.chat.id,
            'Ваше задание отправлено, ждите результата',
            reply_markup=remove_markup()
        )  # TODO add English

        task = Task.get(submission.task_id)
        task_detail_view(student, task)
    elif message.text in ['❌ Отмена', '❌ Cancel']:
        bot.send_message(message.chat.id, 'Отмена', reply_markup=remove_markup())  # TODO add English

        task = Task.get(submission.task_id)
        task_detail_view(student, task)
        submission.delete()
    else:
        submission.add(message)
        bot.send_message(
            message.chat.id,
            'Отправьте ещё что-то или нажмите *Отправить на проверку*',
            reply_markup=markups.get_compose_submission_markup(student),
            parse_mode='Markdown',
        )  # TODO add English
        bot.register_next_step_handler(message, compose_submission, submission)
