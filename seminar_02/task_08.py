"""
Создать страницу, на которой будет форма для ввода имени
и кнопка "Отправить"
При нажатии на кнопку будет произведено
перенаправление на страницу с flash сообщением, где будет
выведено "Привет, {имя}!".
"""

from flask import Flask, request, redirect, render_template, url_for, flash
from markupsafe import escape

app = Flask(__file__)

app.secret_key = b'key'
"""
Генерация надёжного ключа (в консоли)
>>> import secrets
>>> secrets.token_hex()
"""

menu = {'Главная': '/'}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = escape(request.form.get('name'))
        if not name:
            flash('Введите имя', 'danger')
            return redirect(url_for('index'))
        flash(f'Привет, {name}!', 'success')
        return redirect(url_for('index'))

    return render_template('t8_index.html', title="Привет", menu=menu.items())


if __name__ == '__main__':
    app.run(debug=True)
