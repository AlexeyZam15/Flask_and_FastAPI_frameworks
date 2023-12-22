"""
Написать функцию, которая будет выводить на экран HTML
страницу с заголовком "Моя первая HTML страница" и
абзацем "Привет, мир!".
"""

from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def index():
    context = {
        'title': 'Моя первая HTML страница',
        'name': 'Привет, мир!',
    }
    return render_template('task_05.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
