"""
Создать страницу, на которой будет форма для ввода логина
и пароля
При нажатии на кнопку "Отправить" будет произведена
проверка соответствия логина и пароля и переход на
страницу приветствия пользователя или страницу с
ошибкой.
"""

from flask import Flask, request, render_template, session, flash, redirect, url_for
from markupsafe import escape

app = Flask(__file__)

app.secret_key = b'key'
"""
Генерация надёжного ключа (в консоли)
>>> import secrets
>>> secrets.token_hex()
"""


@app.route('/')
def index():
    return render_template('t3_index.html', title="Главная", text="Добро пожаловать на сайт",
                           username=session.get('username'))


@app.route('/reg/', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        if 'accounts' not in session:
            session['accounts'] = {}
        login = escape(request.form.get('login'))
        if not login:
            flash('Введите логин', 'danger')
            return redirect(url_for('registration'))
        if login in session['accounts']:
            flash('Такой логин уже существует', 'danger')
            return redirect(url_for('registration'))
        password = escape(request.form.get('password'))
        if not password:
            flash('Введите пароль', 'danger')
            return redirect(url_for('registration'))
        password2 = escape(request.form.get('password2'))
        if not password2:
            flash('Подтвердите пароль', 'danger')
            return redirect(url_for('registration'))
        if password != password2:
            flash('Пароли не совпадают', 'danger')
            return redirect(url_for('registration'))
        session['accounts'][login] = password
        flash(f'{login}, вы успешно зарегистрировались', 'success')
        session['username'] = login
        return redirect(url_for('index'))
    return render_template('t3_reg.html', title="Регистрация", username=session.get('username'))


@app.route('/auth/', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        login = escape(request.form.get('login'))
        if not login:
            flash('Введите логин', 'danger')
            return redirect(url_for('auth'))
        password = escape(request.form.get('password'))
        if not password:
            flash('Введите пароль', 'danger')
            return redirect(url_for('auth'))
        if login not in session['accounts'] or session['accounts'][login] != password:
            flash('Неверный логин или пароль', 'danger')
            return redirect(url_for('auth'))
        session['username'] = login
        flash(f'{login}, вы успешно авторизовались', 'success')
        return redirect(url_for('index'))

    return render_template('t3_auth.html', title="Авторизация", username=session.get('username'))


@app.route('/logout/')
def log_out():
    session['username'] = None
    flash(f'Вы успешно вышли из аккаунта', 'success')
    return redirect(url_for('index'))


@app.route('/del/', methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        login = escape(request.form['login'])
        if not login:
            flash('Введите логин', 'danger')
            return redirect(url_for('delete'))
        if login != session['username']:
            flash(f'Введённый логин не соответствует имени пользователя', 'danger')
            return redirect(url_for('delete'))
        password = escape(request.form.get('password'))
        if not password:
            flash('Введите пароль', 'danger')
            return redirect(url_for('delete'))
        if login not in session['accounts'] or session['accounts'][login] != password:
            flash('Неверный логин или пароль', 'danger')
            return redirect(url_for('delete'))
        session['accounts'].pop(session['username'])
        session['username'] = None
        flash(f'Вы успешно удалили свой аккаунт', 'success')
        return redirect(url_for('index'))
    return render_template('t3_delete.html', title="Удаление", username=session.get('username'))


if __name__ == '__main__':
    app.run(debug=True)
