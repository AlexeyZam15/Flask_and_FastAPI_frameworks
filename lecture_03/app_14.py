from flask import Flask, render_template
from flask_wtf import FlaskForm

app = Flask(__name__)

menu = {'Главная': '/'}


@app.route('/')
def index():
    context = {'menu': menu.items(),
               'title': 'Главная',
               'text': "Hello, World!"}
    return render_template('index.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
