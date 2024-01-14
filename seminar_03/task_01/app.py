"""
Создать базу данных для хранения информации о студентах университета.
База данных должна содержать две таблицы: "Студенты" и "Факультеты".
В таблице "Студенты" должны быть следующие поля: id, имя, фамилия, возраст, пол, группа и id факультета.
В таблице "Факультеты" должны быть следующие поля: id и название факультета.
Необходимо создать связь между таблицами "Студенты" и "Факультеты".
Написать функцию-обработчик, которая будет выводить список всех
студентов с указанием их факультета.
"""
import random

import pandas as pd
from flask import Flask
from models import db, Student, Faculty

app = Flask(__file__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)


def check_tables():
    """
    Проверка наличия таблицы в базе данных
    """
    try:
        Student.query.all()
        Faculty.query.all()
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
    # Добавляем Факультеты
    for faculty in range(1, count + 1):
        new_faculty = Faculty(name=f'faculty{faculty}')
        db.session.add(new_faculty)
    # Добавляем студентов
    for user in range(1, count + 1):
        new_student = Student(name=f'name{user}', surname=f'surname{user}', age=random.randint(18, 60),
                              gender=random.choice(['male', 'female']), group=f'group{user}',
                              faculty_id=user)
        db.session.add(new_student)
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
        'faculty': student.faculty.name,
    } for student in Student.query.all()]
    if not students:
        return 'Таблица студентов пуста'
    html_table = pd.DataFrame(students).to_html(index=False)
    return html_table


if __name__ == '__main__':
    app.run(debug=True)
