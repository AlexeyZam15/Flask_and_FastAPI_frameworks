"""
Создать страницу, на которой будет изображение и ссылка
на другую страницу, на которой будет отображаться форма
для загрузки изображений.
"""
from pathlib import PurePath, Path

from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.utils import secure_filename

from os import path as os_path

app = Flask(__file__)

app.secret_key = 'key'
"""
Генерация надёжного ключа (в консоли)
>>> import secrets
>>> secrets.token_hex()
"""


@app.route('/')
def index():
    if 'img' not in session:
        session['img'] = '/static/img/foto.jpg'
    return render_template('task_02.html', img=session['img'])


@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        file_name = secure_filename(file.filename)
        if not file:
            return render_template('t2_upload.html', text="Выберите файл!")
        file_ext = os_path.splitext(file.filename)[1].lower()
        if file_ext not in ['.jpg', '.png', '.gif']:
            return render_template('t2_upload.html', text="Файл должен быть форматов jpg, png или gif")
        file.save(PurePath.joinpath(Path.cwd(), 'static/img/', file_name))
        session['img'] = f'/static/img/{file_name}'
        return redirect(url_for('index'))
    return render_template('t2_upload.html')


if __name__ == '__main__':
    app.run(debug=True)
