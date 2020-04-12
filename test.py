from bot import bot
import settings
import requests


@bot.message_handler(content_types=['photo'])
def new_habit(message):
    file_info = bot.get_file(message.photo[2].file_id)

    response = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(settings.BOT_TOKEN, file_info.file_path),
                            proxies={'https': settings.PROXY})
    with open('dino.jpg', 'wb') as f:
        f.write(response.content)
    photo = open('dino.jpg', 'rb')
    bot.send_photo(message.chat.id, photo)
    bot.send_message(message.chat.id, 'OK')
