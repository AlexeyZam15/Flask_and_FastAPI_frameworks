"""
Создать страницу, на которой будет изображение и ссылка
на другую страницу, на которой будет отображаться форма
для загрузки изображений.
"""
from pathlib import PurePath, Path

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__file__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        file_name = secure_filename(file.filename)
        file.save(PurePath.joinpath(Path.cwd(), 'static/img/', file_name))
        img = f'/static/img/{file_name}'
        return render_template('task_02.html', img=img)
    img = '/static/img/foto.jpg'
    return render_template('task_02.html', img=img)


@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    return render_template('t2_upload.html')


if __name__ == '__main__':
    app.run(debug=True)
