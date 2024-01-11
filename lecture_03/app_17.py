from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect

from lecture_03.forms_3 import LoginForm, RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
csrf = CSRFProtect(app)
"""
Генерация надёжного ключа
>>> import secrets
>>> secrets.token_hex()
"""

menu = {'Главная': '/',
        'Войти': '/login/',
        'Регистрация': '/register/'
        }


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
    context = {'menu': menu.items(),
               'title': 'Авторизация',
               'form': form}
    return render_template('login.html', **context)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        # Обработка данных из формы
        email = form.email.data
        password = form.password.data
        print(email, password)
        ...
    context = {'menu': menu.items(),
               'title': 'Регистрация',
               'form': form}
    return render_template('register.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
