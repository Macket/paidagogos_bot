from flask import Flask
from flask import render_template
from flask import request
import time
from bot import bot
import test
import base64
import threading


app = Flask(__name__,
            static_folder='static',
            template_folder='templates')

# app.debug = False
# app.use_reloader=False


@app.route('/')
def hello_world():
    return render_template('drawing.html')


@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        with open('savedCanvas.png', 'wb') as f:
            str_data = request.values.to_dict()['imgBase64']
            f.write(base64.b64decode(str_data[str_data.index(';base64,') + 8:]))

    return 'ok'


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    threading.Thread(target=app.run).start()

    print('after')

    while True:
        try:
            bot.polling(none_stop=True, interval=1, timeout=0)
        except:
            time.sleep(10)
