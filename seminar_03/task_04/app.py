"""
После отправки формы данные должны сохраняться в базе данных (можно использовать SQLite)
и выводиться сообщение об успешной регистрации. Если какое-то из обязательных полей не
заполнено или данные не прошли валидацию, то должно выводиться соответствующее
сообщение об ошибке.
Дополнительно: добавьте проверку на уникальность имени пользователя и электронной почты в
базе данных. Если такой пользователь уже зарегистрирован, то должно выводиться сообщение
об ошибке.
"""
from flask_bcrypt import check_password_hash, generate_password_hash, Bcrypt
from flask import Flask, session, request, render_template, flash, redirect, url_for
from flask_wtf import CSRFProtect

from forms import RegistrationForm

from models import db, User

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.secret_key = b'key'
"""
Генерация надёжного ключа (в консоли)
>>> import secrets
>>> secrets.token_hex()
"""

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)
csrf = CSRFProtect(app)

tables = [User]

menu = {'Главная': '/',
        'Регистрация': '/register/'}


def check_tables():
    """
    Проверка наличия таблицы в базе данных
    """
    try:
        for table in tables:
            table.query.first()
        return True
    except Exception as e:
        print(e)
        return False


@app.cli.command("init-db")
@app.route('/db/init/')
def init_db():
    """
    Создание таблиц в базе данных
    """
    # ошибка с неверным wsgi.py
    db.create_all()
    return 'Таблицы созданы'


@app.cli.command("del-db")
@app.route('/db/del/')
def del_db():
    db.drop_all()
    return 'Таблицы удалены'


@app.route('/')
def index():
    username = session.get('username', 'незнакомец')
    return render_template('index.html', menu=menu.items(), text=f'Привет, {username}')


@app.route('/register/', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        username = form.username.data
        if User.query.filter_by(username=username).first():
            flash('Имя пользователя уже занято', 'danger')
            return redirect(url_for('register'))
        email = form.email.data
        if User.query.filter_by(email=email).first():
            flash('Пользователь с таким email уже существует', 'danger')
            return redirect(url_for('register'))
        password = form.password.data
        password_hash = generate_password_hash(password)
        print(password_hash)
        user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        session['username'] = username
        flash('Вы успешно зарегистрировались', 'success')
        return redirect(url_for('index'))

    context = {'menu': menu.items(),
               'title': 'Регистрация',
               'form': form}

    return render_template('register.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
