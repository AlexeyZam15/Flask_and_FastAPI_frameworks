"""
Создать страницу, на которой будет форма для ввода имени
и возраста пользователя и кнопка "Отправить"
При нажатии на кнопку будет произведена проверка
возраста и переход на страницу с результатом или на
страницу с ошибкой в случае некорректного возраста.
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
        age = escape(request.form.get('age'))
        if not age:
            flash('Введите возраст', 'danger')
            return redirect(url_for('index'))
        try:
            age = int(age)
        except Exception:
            flash('Возраст должен быть целым числом', 'danger')
            return redirect(url_for('index'))
        if age < 18:
            flash('Пользователю должно быть не меньше 18 лет', 'danger')
            return redirect(url_for('index'))
        if age >= 116:
            flash('Сначала запишитесь в книгу рекордов Гинесса. Самому старому человеку сейчас 116 лет.', 'danger')
            return redirect(url_for('index'))
        return redirect(url_for('result', name=name, age=age))
    return render_template('t6_index.html', title="Новый пользователь", menu=menu.items())


@app.route('/res/')
def result():
    name = request.args['name']
    age = request.args['age']
    return render_template('t6_res.html', title="Результат", name=name, age=age, menu=menu.items())


if __name__ == '__main__':
    app.run(debug=True)
