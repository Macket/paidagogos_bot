from bot import bot
from users.models import Teacher, Student
from classrooms.models import Classroom
from classrooms import markups
from users import markups as user_markups
from utils.scripts import get_call_data


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@CLASSROOM/'))
def handle_classroom_query(call):
    data = get_call_data(call)
    show_classroom(call.message, data['classroom_id'], True)


def show_classroom(message, classroom_id, edit=False):
    user = Teacher.get(message.chat.id) or Student.get(message.chat.id)
    if type(user) is Teacher:
        teacher = user
        classroom = Classroom.get(classroom_id)

        if edit:
            bot.edit_message_text(
                f'*{classroom.name}*',
                chat_id=message.chat.id,
                message_id=message.message_id,
                reply_markup=markups.get_teacher_classroom_inline_markup(teacher, classroom),
                parse_mode='Markdown')
        else:
            bot.send_message(
                message.chat.id,
                f'*{classroom.name}*',
                reply_markup=markups.get_teacher_classroom_inline_markup(teacher, classroom),
                parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: call.data.startswith('@@CLASSROOMS/'))
def handle_classrooms_query(call):
    teacher = Teacher.get(call.message.chat.id)
    bot.send_message(call.message.chat.id, 'Классные комнаты',
                     reply_markup=user_markups.get_classrooms_inline_markup(teacher))
