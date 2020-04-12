from flask import Flask
from flask import render_template
from flask import request
import time
from bot import bot
import users.intro
import users.photos
from classrooms.models import Photo
import base64
import threading
import requests
import settings
from database.db_scripts import init_database


init_database()


app = Flask(__name__,
            static_folder='static',
            template_folder='templates')

# app.debug = False
# app.use_reloader=False


@app.route('/')
def hello_world():
    return render_template('drawing.html')


@app.route('/drawer/', methods=['GET', 'POST'])
def drawer():
    if request.method == 'GET':
        file_id = request.args.get('file_id', None)
        file_path = request.args.get('file_path', None)
        file_extension = file_path[file_path.index('.') + 1:]

        response = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(settings.BOT_TOKEN, file_path),
                                proxies={'https': settings.PROXY})
        with open('static/media/{0}.{1}'.format(file_id, file_extension), 'wb') as f:
            f.write(response.content)

        return render_template('drawing.html', file_id=file_id, file_extension=file_extension)

    if request.method == 'POST':
        data = request.values.to_dict()
        image_str = data['imgBase64']
        filename = data['filename']
        fileId = data['fileId']
        # image_bytes = base64.b64decode(image_str[image_str.index(';base64,') + 8:])
        # with open(filename, 'wb') as f:
        #     f.write(image_bytes)
        photo = open(filename, 'rb')

        student_id = Photo.get(fileId).student_id
        print('STUDENT')
        print(student_id)

        bot.send_photo(student_id, photo)

        return 'ok'


# @app.route('/upload/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         with open('savedCanvas.png', 'wb') as f:
#             str_data = request.values.to_dict()['imgBase64']
#             f.write(base64.b64decode(str_data[str_data.index(';base64,') + 8:]))
#
#     return 'ok'


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    threading.Thread(target=app.run).start()

    print('after')

    while True:
        try:
            bot.polling(none_stop=True, interval=1, timeout=0)
        except:
            time.sleep(10)
