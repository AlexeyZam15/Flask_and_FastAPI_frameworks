from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect

from lecture_03.forms_3 import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
csrf = CSRFProtect(app)
"""
Генерация надёжного ключа
>>> import secrets
>>> secrets.token_hex()
"""

menu = {'Главная': '/',
        'Войти': '/login/'}


@app.route('/')
def index():
    context = {'menu': menu.items(),
               'title': 'Главная',
               'content': "Hello, World!"}
    return render_template('index.html', **context)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        # Обработка данных из формы
        pass
    return render_template('login.html', form=form, menu=menu.items())


if __name__ == '__main__':
    app.run(debug=True)
