from bot import bot
from classrooms.models import Classroom
from users.models import Teacher, Student
from tasks.models import Task, Submission, SubmissionStatus
from datetime import datetime, timezone
from tasks.scenarios import create_task_scenario, create_submission_scenario, review_submission_scenario
from classrooms.views import task_assessments_view
from tasks.views import task_list_view, task_detail_view, task_message_list_view, \
    submission_list_view, submission_message_list_view, submission_review_result_view
from utils.scripts import get_call_data


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@TASKS/'))
def handle_tasks_query(call):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    data = get_call_data(call)
    user = Teacher.get(call.message.chat.id) or Student.get(call.message.chat.id)
    classroom = Classroom.get(data['classroom_id'])
    task_list_view(user, classroom, message_to_edit=call.message)


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@TASK/'))
def handle_task_query(call):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    data = get_call_data(call)
    user = Teacher.get(call.message.chat.id) or Student.get(call.message.chat.id)
    task = Task.get(data['task_id'])
    task_detail_view(user, task, message_to_edit=call.message)


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@TASK_MESSAGES/'))
def handle_task_messages_query(call):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    data = get_call_data(call)
    user = Teacher.get(call.message.chat.id) or Student.get(call.message.chat.id)
    task = Task.get(data['task_id'])
    task_message_list_view(user, task)
    task_detail_view(user, task)


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@NEW_TASK/'))
def handle_new_task_query(call):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    data = get_call_data(call)
    create_task_scenario.task_name_request(call.message, data['classroom_id'])


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@SUBMISSIONS_FOR_REVIEW/'))
def handle_submissions_for_review_query(call):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    data = get_call_data(call)
    teacher = Teacher.get(call.message.chat.id)
    task = Task.get(data['task_id'])
    submission_list_view(teacher, task, message_to_edit=call.message)


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@SUBMISSIONS_REVIEWED/'))
def handle_submissions_reviewed_query(call):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    data = get_call_data(call)
    teacher = Teacher.get(call.message.chat.id)
    task = Task.get(data['task_id'])
    task_assessments_view(teacher, task)
    task_detail_view(teacher, task)


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@SUBMISSION_MESSAGES/'))
def handle_submission_message_list_query(call):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    data = get_call_data(call)
    user = Teacher.get(call.message.chat.id) or Student.get(call.message.chat.id)
    submission = Submission.get(data['submission_id'])
    task = Task.get(submission.task_id)
    submission_message_list_view(user, submission, task)
    task_detail_view(user, task, message_to_edit=call.message)


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@SUBMISSION_REVIEW/'))
def handle_submission_review_query(call):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    data = get_call_data(call)

    user = Teacher.get(call.message.chat.id) or Student.get(call.message.chat.id)
    submission = Submission.get(data['submission_id'])
    task = Task.get(submission.task_id)

    submission_message_list_view(user, submission, task)
    review_submission_scenario.submission_comment_request(call.message, data['submission_id'])


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@SUBMISSION_REVIEW_RESULT/'))
def handle_submission_review_result_query(call):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    data = get_call_data(call)

    submission = Submission.get(data['submission_id'])
    task = Task.get(submission.task_id)
    user = Teacher.get(call.message.chat.id) or Student.get(call.message.chat.id)

    submission_review_result_view(user, submission, task)
    task_detail_view(user, task)


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@NEW_SUBMISSION/'))
def handle_new_submission_query(call):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    data = get_call_data(call)

    student = Student.get(call.message.chat.id)
    submission = Submission(
        data['task_id'],
        student.id,
        status=SubmissionStatus.DRAFT.value,
        created_utc=datetime.now(timezone.utc)
    ).save()

    ru_text = "Отправьте мне выполненное задание в любом формате: " \
              "текст, фото, видео, файлы или аудиосообщения; одним или несколькими сообщениями."
    en_text = None
    text = ru_text if student.language_code == 'ru' else en_text

    bot.send_message(call.message.chat.id,
                     text,
                     parse_mode='Markdown')
    bot.register_next_step_handler(call.message, create_submission_scenario.compose_submission, submission)
