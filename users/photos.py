from bot import bot
from users.models import Teacher
from tasks.markups import get_drawer_markup


@bot.message_handler(content_types=['photo'])
def new_photo(message):
    teacher = Teacher.get(message.chat.id)
    if teacher:
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_photo(
            teacher.id,
            message.photo[-1].file_id,
            caption='Нажми, чтобы исправить ошибки👇🏻',  # TODO add English
            reply_markup=get_drawer_markup(message.photo[-1].file_id, message.chat.id)
        )
