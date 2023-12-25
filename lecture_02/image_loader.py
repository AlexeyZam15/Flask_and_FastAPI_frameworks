"""html страница, загружающая файл в папку uploads"""
import os
from flask import Flask, request, render_template

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'uploads')
if not os.path.exists(app.config['UPLOAD_PATH']):
    os.makedirs(app.config['UPLOAD_PATH'])
    print(f"Создана папка {app.config['UPLOAD_PATH']}")

upload_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Загрузка файла</title>
</head>
<body>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Загрузить">
    </form>
</body>
</html>
"""


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            file_ext = os.path.splitext(file.filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                return upload_html.replace("</body>", """   <p>Неверный формат файла</p>
</body>""")
            file.save(os.path.join(app.config['UPLOAD_PATH'], file.filename))
            return f"Файл {file.filename} загружен на сервер"
    return upload_html


if __name__ == '__main__':
    app.run(debug=True)
