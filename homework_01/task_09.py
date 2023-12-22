"""
Создать базовый шаблон для интернет-магазина,
содержащий общие элементы дизайна (шапка, меню,
подвал), и дочерние шаблоны для страниц категорий
товаров и отдельных товаров.
Например, создать страницы "Одежда", "Обувь" и "Куртка",
используя базовый шаблон.
"""
import json

from flask import Flask, render_template

app = Flask(__name__)

with open('static/json/goods.json', 'r', encoding='utf-8') as file:
    goods = json.load(file)


@app.route('/')
def main():
    context = {
        'title': 'Главная',
        'text': 'Главная страница'
    }
    return render_template('index.html', **context)


@app.route('/clothes/')
def clothes():
    context = {
        'title': 'Одежда',
        'goods': goods["goods"]
    }
    return render_template('clothes.html', **context)


@app.route('/shoes/')
def shoes():
    context = {
        'title': 'Обувь',
        'goods': goods["goods"]
    }
    return render_template('shoes.html', **context)


@app.route('/jacket/')
def jacket():
    context = {
        'title': 'Куртки',
        'goods': goods["goods"]
    }
    return render_template('jackets.html', **context)


@app.route('/<clothes_type>/')
def clothes_type_page(clothes_type: str):
    c_goods = [good for good in goods["goods"] if good["type"] == clothes_type]
    context = {
        'title': f"Одежда типа {clothes_type.capitalize()}",
        'goods': c_goods
    }
    if c_goods:
        return render_template('clothes.html', **context)
    context = {
        'title': 'Главная',
        'text': f'Одежды типа {clothes_type} нет в наличии'
    }
    return render_template('index.html', **context)


if __name__ == '__main__':
    # print(goods)
    # for good in goods:
    #     print(good)
    #     print(good['name'])
    #     print(good['img'])
    #     print(good['description'])
    app.run(debug=True)
