import time
from bot import bot
from users import intro
from users import photos
from classrooms import handlers
from tasks import handlers
from database.db_scripts import init_database

init_database()

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True, interval=1, timeout=0)
        except:
            time.sleep(10)
