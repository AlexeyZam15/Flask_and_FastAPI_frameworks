"""
Создать страницу, на которой будет форма для ввода текста и
кнопка "Отправить"
При нажатии кнопки будет произведен подсчет количества слов
в тексте и переход на страницу с результатом.
"""

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__file__)


@app.route('/')
def index():
    return render_template('t4_index.html')


@app.route('/count/', methods=['GET', 'POST'])
def count():
    if request.method == 'POST':
        text = request.form.get('text')
        words = len(text.split())
        return f"В тексте слов: {words}"
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
