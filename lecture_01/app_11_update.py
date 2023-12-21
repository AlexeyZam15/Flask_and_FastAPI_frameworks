from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/main/')
def main():
    context = {'title': 'Главная'}
    return render_template('new_main.html', **context)


@app.route('/data/')
def data():
    context = {'title': 'База статей'}
    return render_template('new_data.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
