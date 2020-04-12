from telebot import types
from bot import bot
from users.models import Student, User
from classrooms.models import Classroom, Photo
import settings


def get_drawer_markup(file_id, file_path):

    inline_markup = types.InlineKeyboardMarkup(row_width=1)

    url = f'http://127.0.0.1:5000/drawer/?file_id={file_id}&file_path={file_path}' if settings.DEBUG \
        else f'https://127.0.0.1:5000/drawer/?file_id={file_id}&file_path={file_path}'  # TODO
    inline_markup.add(
        types.InlineKeyboardButton(text='Make notes', url=url),
    )

    return inline_markup


@bot.message_handler(content_types=['photo'])
def new_photo(message):
    student = Student.get(message.chat.id)
    print('SOMETHING!!!')
    if student:
        file_info = bot.get_file(message.photo[2].file_id)
        teacher = User.get(Classroom.get(student.classroom_id).teacher_id)
        Photo(file_info.file_id, student.id, teacher.id).save()

        bot.send_photo(teacher.id, file_info.file_id)
        bot.send_message(teacher.id, f'Homework from Nastya. Click this button to make some notes', reply_markup=get_drawer_markup(file_info.file_id, file_info.file_path))
