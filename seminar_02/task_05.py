"""
Создать страницу, на которой будет форма для ввода двух
чисел и выбор операции (сложение, вычитание, умножение
или деление) и кнопка "Вычислить"
При нажатии на кнопку будет произведено вычисление
результата выбранной операции и переход на страницу с
результатом.
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from markupsafe import escape

app = Flask(__file__)

app.secret_key = b'key'
"""
Генерация надёжного ключа (в консоли)
>>> import secrets
>>> secrets.token_hex()
"""

operations = {'сложение': '+',
              'вычитание': '-',
              'умножение': '*',
              'деление': '/'}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        numb1 = request.form.get('number1')
        if not numb1:
            flash('Введите первое число', 'danger')
            return redirect(url_for('index'))
        numb2 = request.form.get('number2')
        if not numb2:
            flash('Введите второе число', 'danger')
            return redirect(url_for('index'))
        operation = escape(request.form.get('operation').lower())
        if not operation or operation not in operations:
            flash('Выберите операцию из списка', 'danger')
            return redirect(url_for('index'))
        res = eval(f'{numb1} {operations[operation]} {numb2}')
        return redirect(url_for('result', res=res))

    return render_template('t5_index.html', title='Главная')


@app.route('/res/', methods=['GET', 'POST'])
def result():
    res = request.args['res']
    return render_template('t5_result.html', title="Результат", res=res)


if __name__ == '__main__':
    app.run(debug=True)
