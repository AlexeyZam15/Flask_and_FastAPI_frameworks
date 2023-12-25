from flask import Flask, make_response, render_template

app = Flask(__file__)


@app.route('/')
def index():
    context = {
        'title': 'Главная',
        'name': 'Харитон'
    }
    response = make_response(render_template('main.html', **context))
    response.headers['new_head'] = 'New value'
    response.set_cookie('username', context['name'])
    return response


if __name__ == '__main__':
    app.run(debug=True)
