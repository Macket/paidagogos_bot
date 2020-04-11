from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__,
            static_folder='static',
            template_folder='templates')


@app.route('/')
def hello_world():
    return render_template('drawing.html')


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)


@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print(request.data)

    return 'ok'
