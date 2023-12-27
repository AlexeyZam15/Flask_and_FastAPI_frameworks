"""
Создать страницу, на которой будет кнопка "Нажми меня", при
нажатии на которую будет переход на другую страницу с
приветствием пользователя по имени.
"""

from flask import Flask, request, render_template
from markupsafe import escape

app = Flask(__file__)


@app.route('/', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        name = request.form.get('name')
        if not name:
            return render_template('task_01.html', text="Введите имя!")
        return f'Привет, {escape(name)}!'
    return render_template('task_01.html')


if __name__ == '__main__':
    app.run(debug=True)
