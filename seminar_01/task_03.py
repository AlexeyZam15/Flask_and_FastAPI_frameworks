"""
Flask. Написать функцию, которая будет принимать на вход два
числа и выводить на экран их сумму.
"""
from flask import Flask

app = Flask(__name__)


@app.route('/<a>+<b>')
def sum(a: str, b: str):
    """
    Функция принимает 2 строки, a и b.
    Преобразовывает в целые или вещественные числа, иначе выводит ошибку.
    Выполняет сложение этих чисел.
    """
    try:
        a = int(a)
        b = int(b)
    except ValueError:
        try:
            a = float(a)
            b = float(b)
        except ValueError:
            return f'{a}+{b} - Параметры должны быть целыми или вещественными числами'
    return f'{a} + {b} = {a + b}'


if __name__ == '__main__':
    app.run(debug=True)
