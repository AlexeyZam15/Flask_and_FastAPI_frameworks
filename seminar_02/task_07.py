"""
Создать страницу, на которой будет форма для ввода числа
и кнопка "Отправить"
При нажатии на кнопку будет произведено
перенаправление на страницу с результатом, где будет
выведено введенное число и его квадрат.
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
        number = escape(request.form.get('number'))
        if not number:
            flash('Введите число', 'danger')
            return redirect(url_for('index'))
        try:
            number = int(number)
        except Exception:
            flash('Введите целое число', 'danger')
            return redirect(url_for('index'))
        return redirect(url_for('result', number=number, res=number ** 2))

    return render_template('t7_index.html', title="Ввод числа", menu=menu.items())


@app.route('/res/')
def result():
    number = request.args['number']
    res = request.args['res']
    return render_template('t7_res.html', title="Результат", number=number, res=res, menu=menu.items())


if __name__ == '__main__':
    app.run(debug=True)
