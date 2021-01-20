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

        ru_text = "Ваше задание отправлено, ждите результата"
        en_text = "Your submission is sent, wait for the review result"
        text = ru_text if student.language_code == 'ru' else en_text

        bot.send_message(message.chat.id, text, reply_markup=remove_markup())

        task = Task.get(submission.task_id)
        task_detail_view(student, task)
    elif message.text in ['❌ Отмена', '❌ Cancel']:
        ru_text = "Отмена"
        en_text = "Cancel"
        text = ru_text if student.language_code == 'ru' else en_text

        bot.send_message(message.chat.id, text, reply_markup=remove_markup())

        task = Task.get(submission.task_id)
        task_detail_view(student, task)
        submission.delete()
    else:
        submission.add(message)

        ru_text = "Отправьте ещё что-то или нажмите *Отправить на проверку*"
        en_text = "Send something else or tap *Submit for review*"
        text = ru_text if student.language_code == 'ru' else en_text

        bot.send_message(
            message.chat.id,
            text,
            reply_markup=markups.get_compose_submission_markup(student),
            parse_mode='Markdown',
        )

        bot.register_next_step_handler(message, compose_submission, submission)
