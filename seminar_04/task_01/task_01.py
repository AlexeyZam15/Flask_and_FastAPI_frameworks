"""
Написать программу, которая считывает список из 10 URL адресов и одновременно загружает данные с каждого
адреса.
После загрузки данных нужно записать их в отдельные
файлы.
Используйте потоки.
"""
from threading import Thread

import time

from requests import get

urls = ['https://www.google.ru/',
        'https://gb.ru/',
        'https://ya.ru/',
        'https://www.python.org/',
        'https://habr.com/ru/all/',
        'https://www.reddit.com/',
        'https://www.wikipedia.org/',
        'https://www.lenta.ru/',
        'https://www.youtube.com/'
        'https://www.twitch.tv/'
        ]


def download(url):
    response = get(url)
    filename = 'threading_' + url.replace('https://', '').replace('.', '_').replace('/', '') + '.html'
    with open(filename, "w", encoding='utf-8') as f:
        f.write(response.text)
    print(f"Downloaded {url} in {time.time() - start_time:.2f}seconds")


threads = []
start_time = time.time()

for url in urls:
    thread = Thread(target=download, args=[url])
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
