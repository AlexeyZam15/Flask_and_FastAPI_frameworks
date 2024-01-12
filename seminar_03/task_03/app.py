"""
Доработаем задача про студентов
Создать базу данных для хранения информации о студентах и их оценках в
учебном заведении.
База данных должна содержать две таблицы: "Студенты" и "Оценки".
В таблице "Студенты" должны быть следующие поля: id, имя, фамилия, группа
и email.
В таблице "Оценки" должны быть следующие поля: id, id студента, название
предмета и оценка.
Необходимо создать связь между таблицами "Студенты" и "Оценки".
Написать функцию-обработчик, которая будет выводить список всех
студентов с указанием их оценок.
"""
from random import randint, choice

import pandas as pd
from flask import Flask
from models import db, Student, Mark

app = Flask(__file__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)

tables = [Student, Mark]


def check_tables():
    """
    Проверка наличия таблицы в базе данных
    """
    try:
        for table in tables:
            table.query.first()
        return True
    except Exception as e:
        print(e)
        return False


@app.cli.command("init-db")
@app.route('/db/init/')
def init_db():
    """
    Создание таблиц в базе данных
    """
    # ошибка с неверным wsgi.py
    db.create_all()
    return 'Таблицы созданы'


@app.cli.command("fill-db")
@app.route('/db/fill/')
def fill_tables():
    count = 5
    # Добавляем студентов
    for student in range(1, count + 1):
        new_student = Student(name=f'name{student}', surname=f'surname{student}', age=randint(18, 60),
                              gender=choice(['male', 'female']), group=f'group{student}')
        db.session.add(new_student)
    db.session.commit()
    # Добавляем оценки
    for mark in range(1, count + 1):
        new_mark = Mark(student_id=randint(1, count), subject=f'subject{mark}', mark=randint(1, 5))
        db.session.add(new_mark)
    db.session.commit()
    return 'Таблицы заполнены'


@app.cli.command("del-db")
@app.route('/db/del/')
def del_db():
    db.drop_all()
    return 'Таблицы удалены'


@app.route('/', methods=['GET', 'POST'])
def index():
    if not check_tables():
        return 'Таблицы не созданы'
    students = [{
        'id': student.id,
        'name': student.name,
        'surname': student.surname,
        'age': student.age,
        'gender': student.gender,
        'group': student.group,
        'marks': ", ".join([mark.subject + ': ' + str(mark.mark)
                           for mark in student.marks])
    } for student in Student.query.all()]
    if not students:
        return 'Таблица студентов пуста'
    html_table = pd.DataFrame(students).to_html(index=False)
    return html_table


if __name__ == '__main__':
    app.run(debug=True)
