"""
Написать функцию, которая будет выводить на экран HTML
страницу с блоками новостей.
Каждый блок должен содержать заголовок новости,
краткое описание и дату публикации.
Данные о новостях должны быть переданы в шаблон через
контекст.
"""

from flask import Flask, render_template

app = Flask(__name__)

news = [
    {'new_id': 1, 'title': 'Новость 1', 'description': 'Описание новости 1', 'date': '01.01.2022',
     'full_description': 'Полное описание новости 1'},
    {'new_id': 2, 'title': 'Новость 2', 'description': 'Описание новости 2', 'date': '02.01.2022',
     'full_description': 'Полное описание новости 2'},
    {'new_id': 3, 'title': 'Новость 3', 'description': 'Описание новости 3', 'date': '03.01.2022',
     'full_description': 'Полное описание новости 3'},
    {'new_id': 4, 'title': 'Новость 4', 'description': 'Описание новости 4', 'date': '04.01.2022',
     'full_description': 'Полное описание новости 4'},
    {'new_id': 5, 'title': 'Новость 5', 'description': 'Описание новости 5', 'date': '05.01.2022',
     'full_description': 'Полное описание новости 5'},
    {'new_id': 6, 'title': 'Новость 6', 'description': 'Описание новости 6', 'date': '06.01.2022',
     'full_description': 'Полное описание новости 6'},
]


def get_by_new_id(key_value):
    return_list = []
    for new in news:
        if new['new_id'] == key_value:
            return new


@app.route('/news/<new_id>')
def new_page(new_id):
    try:
        new_id = int(new_id)
    except ValueError:
        return 'Номер новости должен быть целым числом'
    new = get_by_new_id(new_id)
    try:
        return render_template('task_07_new.html', **new)
    except IndexError:
        return f'Новость под номером {new_id} не найдена'


@app.route('/news/')
def news_page():
    return render_template('task_07_news.html', news=news)


if __name__ == '__main__':
    app.run(debug=True)
