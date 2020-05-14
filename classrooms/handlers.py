from bot import bot
from users.models import Teacher, Student
from classrooms.models import Classroom
from classrooms.views import classroom_detail_view, classroom_list_view, classroom_link_view, \
    classroom_student_list_view, classroom_assessments_view
from classrooms.scenarios import rename_classroom_scenario, delete_classroom_scenario, create_classroom_scenario
from utils.scripts import get_call_data


@bot.message_handler(commands=['classrooms'])
def handle_classrooms_command(message):
    user = Teacher.get(message.chat.id) or Student.get(message.chat.id)
    classroom_list_view(user)


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@CLASSROOMS/'))
def handle_classrooms_query(call):
    user = Teacher.get(call.message.chat.id) or Student.get(call.message.chat.id)
    classroom_list_view(user, message_to_edit=call.message)


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@CLASSROOM/'))
def handle_classroom_query(call):
    data = get_call_data(call)
    user = Teacher.get(call.message.chat.id) or Student.get(call.message.chat.id)
    classroom = Classroom.get(data['classroom_id'])
    classroom_detail_view(user, classroom, message_to_edit=call.message)


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@CLASSROOM_STUDENTS/'))
def handle_classroom_students_query(call):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    data = get_call_data(call)
    teacher = Teacher.get(call.message.chat.id)
    classroom = Classroom.get(data['classroom_id'])
    classroom_student_list_view(teacher, classroom)
    classroom_detail_view(teacher, classroom)


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@CLASSROOM_LINK/'))
def handle_classroom_link_query(call):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    data = get_call_data(call)
    teacher = Teacher.get(call.message.chat.id)
    classroom = Classroom.get(data['classroom_id'])
    classroom_link_view(teacher, classroom)
    classroom_detail_view(teacher, classroom)


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@CLASSROOM_RENAME/'))
def handle_classroom_rename_query(call):
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
    classroom_assessments_view(student, classroom)
    classroom_detail_view(student, classroom)


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@NEW_CLASSROOM/'))
def handle_new_classroom_query(call):
    bot.clear_step_handler_by_chat_id(call.message.chat.id)
    create_classroom_scenario.classroom_name_request(call.message)
