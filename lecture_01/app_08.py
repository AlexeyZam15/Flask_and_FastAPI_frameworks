from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/if/')
def index():
    context = {
        'title': 'Ветвление',
        'user': 'Крутой хакер',
        'number': 1,
    }
    return render_template('show_if.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
