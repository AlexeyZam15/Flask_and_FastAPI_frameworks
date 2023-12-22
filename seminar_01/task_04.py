"""
Написать функцию, которая будет принимать на вход строку и
выводить на экран ее длину.
"""

from flask import Flask

app = Flask(__name__)


@app.route('/<string>/')
def string_len(string: str):
    return f'Длина строки "{string}" = {len(string)} символов'


if __name__ == '__main__':
    app.run(debug=True)
