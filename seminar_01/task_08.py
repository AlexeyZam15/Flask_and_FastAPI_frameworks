"""
Создать базовый шаблон для всего сайта, содержащий
общие элементы дизайна (шапка, меню, подвал), и
дочерние шаблоны для каждой отдельной страницы.
Например, создать страницу "О нас" и "Контакты",
используя базовый шаблон.
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def main():
    context = {
        'title': 'Главная страница',
        'text': 'Текст главной страницы'
    }
    return render_template('t8_index.html', **context)


@app.route('/about/')
def about():
    context = {
        'title': 'О нас',
        'text': 'Текст страницы О нас'
    }
    return render_template('t8_about.html', **context)


@app.route('/contacts/')
def contacts():
    context = {
        'title': 'Контакты',
        'text': 'Текст страницы Контакты'
    }
    return render_template('t8_contacts.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
