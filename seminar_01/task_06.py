"""
Написать функцию, которая будет выводить на экран HTML
страницу с таблицей, содержащей информацию о студентах.
Таблица должна содержать следующие поля: "Имя",
"Фамилия", "Возраст", "Средний балл".
Данные о студентах должны быть переданы в шаблон через
контекст.
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/students/')
def students_table():
    context = {'title': "Таблица студентов",
               'columns': ['Имя', 'Фамилия', 'Возраст', 'Средний балл'],
               'students': [
                   {'name': 'Иван', 'surname': 'Иванов', 'age': 20, 'avg_score': 4.5},
                   {'name': 'Петр', 'surname': 'Петров', 'age': 22, 'avg_score': 5.0},
                   {'name': 'Сергей', 'surname': 'Сергеев', 'age': 19, 'avg_score': 4.8},
               ]}
    return render_template('task_06.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
