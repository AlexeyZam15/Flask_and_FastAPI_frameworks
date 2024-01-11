from flask import Flask, render_template
from models_05 import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)

menu = {'Главная': '/',
        'Пользователи': '/users/'}


@app.route('/')
def index():
    context = {'menu': menu.items(),
               'title': 'Главная',
               'text': "Hello, World!"}
    return render_template('index.html', **context)


@app.route('/users/')
def all_users():
    users = User.query.all()
    context = {'users': users,
               'menu': menu.items(),
               'title': 'Пользователи'}
    return render_template('users.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
