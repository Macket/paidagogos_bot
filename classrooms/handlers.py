from bot import bot
from users.models import Teacher, Student
from classrooms.models import Classroom
from datetime import datetime, timezone
from classrooms.views import classroom_detail_view, classroom_list_view, classroom_link_view, \
    classroom_student_list_view, classroom_assessments_view
from classrooms.scenarios import rename_classroom_scenario, delete_classroom_scenario
from utils.scripts import get_call_data


@bot.message_handler(commands=['classrooms'])
def handle_classrooms_command(message):
    classroom_list_view(message)


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@CLASSROOMS/'))
def handle_classrooms_query(call):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    classroom_list_view(call.message, edit=True)


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@CLASSROOM/'))
def handle_classroom_query(call):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    data = get_call_data(call)
    classroom_detail_view(call.message, data['classroom_id'], edit=True)


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@CLASSROOM_STUDENTS/'))
def handle_classroom_query(call):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    data = get_call_data(call)
    classroom_student_list_view(call.message, data['classroom_id'])
    classroom_detail_view(call.message, data['classroom_id'])


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@CLASSROOM_LINK/'))
def handle_classroom_query(call):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    data = get_call_data(call)
    classroom_link_view(call.message, data['classroom_id'])
    classroom_detail_view(call.message, data['classroom_id'])


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@CLASSROOM_RENAME/'))
def handle_classroom_query(call):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    data = get_call_data(call)
    classroom = Classroom.get(data['classroom_id'])
    teacher = Teacher.get(call.message.chat.id)
    rename_classroom_scenario.classroom_name_request(call.message, teacher, classroom)


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@CLASSROOM_DELETE/'))
def handle_classroom_query(call):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    data = get_call_data(call)
    classroom = Classroom.get(data['classroom_id'])
    teacher = Teacher.get(call.message.chat.id)
    delete_classroom_scenario.are_you_sure_request(call.message, teacher, classroom)


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@CLASSROOM_ASSESSMENTS/'))
def handle_classroom_assessments_query(call):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    data = get_call_data(call)
    student = Student.get(call.message.chat.id)
    classroom = Classroom.get(data['classroom_id'])
    classroom_assessments_view(call.message, student, classroom)
    classroom_detail_view(call.message, classroom.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@NEW_CLASSROOM/'))
def handle_new_classroom_query(call):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    classroom_name_request(call.message)


def classroom_name_request(message):
    teacher = Teacher.get(message.chat.id)

    ru_text = f"Отправьте название класса"
    en_text = None
    text = ru_text if teacher.language_code == 'ru' else en_text

    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, classroom_name_receive)


def classroom_name_receive(message):
    teacher = Teacher.get(message.chat.id)
    classroom = Classroom(teacher.id, message.text, created_utc=datetime.now(timezone.utc)).save()

    classroom_link_view(message, classroom.id)
    classroom_list_view(message)
