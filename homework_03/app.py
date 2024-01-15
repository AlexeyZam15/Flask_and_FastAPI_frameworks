"""
Создать форму для регистрации пользователей на сайте.
Форма должна содержать поля "Имя", "Фамилия", "Email", "Пароль" и кнопку "Зарегистрироваться".
При отправке формы данные должны сохраняться в базе данных, а пароль должен быть зашифрован.
"""
from flask_bcrypt import check_password_hash, generate_password_hash, Bcrypt
from flask import Flask, session, render_template, flash, redirect, url_for
from flask_wtf import CSRFProtect

from forms import RegistrationForm, LoginForm

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
        'Регистрация': '/register/',
        'Вход': '/login/',
        'Выход': '/logout/'}


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


def check_auth():
    """
    Проверка авторизации пользователя
    """
    if 'name' in session:
        return True
    return False


def change_menu(status: bool):
    """
    Изменение меню
    """
    if status:
        menu.pop('Регистрация', None)
        menu.pop('Вход', None)
        menu['Выход'] = '/logout/'
    else:
        menu.pop('Выход', None)
        menu['Вход'] = '/login/'
        menu['Регистрация'] = '/register/'
    return menu


@app.cli.command("init-db")
def init_db_cmd():
    """
    Создание таблиц в базе данных
    """
    db.create_all()


@app.route('/db/init/')
def init_db():
    init_db_cmd()
    flash('Таблицы созданы', 'success')
    return redirect(url_for('index'))


@app.cli.command("del-db")
def del_db_cmd():
    """
    Удаление базы данных
    """
    db.drop_all()


@app.route('/db/del/')
def delete_tables():
    del_db_cmd()
    flash('Таблицы удалены', 'success')
    return redirect(url_for('logout'))


@app.route('/')
def index():
    change_menu(check_auth())
    name = session.get('name', 'незнакомец')
    return render_template('index.html', menu=menu.items(), text=f'Привет, {name}')


@app.route('/register/', methods=['POST', 'GET'])
def register():
    if check_auth():
        flash('Вы уже авторизованы', 'danger')
        return redirect(url_for('index'))
    if not check_tables():
        init_db_cmd()
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        if User.query.filter_by(email=email).first():
            flash('Пользователь с таким email уже существует', 'danger')
            return redirect(url_for('register'))
        name = form.name.data
        surname = form.surname.data
        password = form.password.data
        password_hash = generate_password_hash(password)
        user = User(name=name, surname=surname, email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        session['name'] = name
        flash('Вы успешно зарегистрировались', 'success')
        return redirect(url_for('index'))

    context = {'menu': menu.items(),
               'title': 'Регистрация',
               'form': form}

    return render_template('register.html', **context)


@app.route('/logout/')
def logout():
    if not check_auth():
        flash('Вы не авторизованы', 'danger')
        return redirect(url_for('index'))
    session.pop('name', None)
    return redirect(url_for('index'))


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if check_auth():
        flash('Вы уже авторизованы', 'danger')
        return redirect(url_for('index'))
    if not check_tables():
        init_db_cmd()
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        query = User.query.filter_by(email=email).first()
        if not query:
            flash('Пользователь с таким email не найден', 'danger')
            return redirect(url_for('login'))
        password = form.password.data
        if not check_password_hash(query.password_hash, password):
            flash('Неверный пароль', 'danger')
            return redirect(url_for('login'))
        session['name'] = query.name
        flash('Вы успешно авторизовались', 'success')
        return redirect(url_for('index'))

    context = {'menu': menu.items(),
               'title': 'Авторизация',
               'form': form}

    return render_template('login.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
