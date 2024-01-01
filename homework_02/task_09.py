"""
Создать страницу, на которой будет форма для ввода имени и электронной почты.
При отправке которой будет создан cookie файл с данными пользователя
Также будет произведено перенаправление на страницу
приветствия, где будет отображаться имя пользователя.
На странице приветствия должна быть кнопка "Выйти"
При нажатии на кнопку будет удален cookie файл с данными
пользователя и произведено перенаправление на страницу
ввода имени и электронной почты.
"""

from flask import Flask, request, redirect, render_template, url_for, flash, make_response
from markupsafe import escape

app = Flask(__file__)

app.secret_key = b'key'
"""
Генерация надёжного ключа (в консоли)
>>> import secrets
>>> secrets.token_hex()
"""

menu = {'Войти': '/'}


@app.route('/', methods=['GET', 'POST'])
def index():
    name = request.cookies.get('username')
    email = request.cookies.get('email')

    if name and email:
        if 'Войти' in menu:
            menu.pop('Войти')
        if 'Выйти' not in menu:
            menu['Выйти'] = url_for('logout')
        return render_template('t9_index.html', title="Главная", menu=menu.items(), name=name)

    if 'Войти' not in menu:
        menu['Войти'] = url_for('index')

    if request.method == 'POST':
        name = escape(request.form.get('name'))
        if not name:
            flash('Введите имя', 'danger')
            return redirect(url_for('index'))
        email = escape(request.form.get('email'))
        if not email:
            flash('Введите email', 'danger')
            return redirect(url_for('index'))
        response = make_response(redirect(url_for('index')))
        response.set_cookie('username', name)
        response.set_cookie('email', email)
        flash(f'Вы вошли в систему', 'success')
        return response

    return render_template('t9_index.html', title="Авторизация", menu=menu.items(), name=name)


@app.route('/logout/')
def logout():
    response = make_response(redirect(url_for('index')))
    response.delete_cookie('username')
    response.delete_cookie('email')
    if 'Выйти' in menu:
        menu.pop('Выйти')
    flash(f'Вы вышли из системы', 'success')
    return response


if __name__ == '__main__':
    app.run(debug=True)
