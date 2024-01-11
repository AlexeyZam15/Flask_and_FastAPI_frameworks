from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
csrf = CSRFProtect(app)
"""
Генерация надёжного ключа
>>> import secrets
>>> secrets.token_hex()
"""

menu = {'Главная': '/'}


@app.route('/')
def index():
    context = {'menu': menu.items(),
               'title': 'Главная',
               'text': "Hello, World!"}
    return render_template('index.html', **context)


@app.route('/form', methods=['GET', 'POST'])
@csrf.exempt
def my_form():
    ...
    return 'No CSRF protection!'


if __name__ == '__main__':
    app.run(debug=True)
