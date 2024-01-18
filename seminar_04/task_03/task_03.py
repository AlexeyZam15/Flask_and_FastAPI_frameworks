"""
Написать программу, которая считывает список из 10 URL адресов и одновременно загружает данные с каждого
адреса.
После загрузки данных нужно записать их в отдельные
файлы.
Используйте асинхронный подход.
"""

from asyncio import ensure_future, gather, get_event_loop
from aiohttp import ClientSession
import time

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

start_time = time.time()


async def download(url):
    async with ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
            filename = url.replace('https://', '').replace('.', '_').replace('/', '') + '.html'
            with open(filename, "w", encoding='utf-8') as f:
                f.write(text)
            print(f"Downloaded {url} in {time.time() - start_time:.2f}seconds")


async def main():
    tasks = []
    for url in urls:
        task = ensure_future(download(url))
        tasks.append(task)
    await gather(*tasks)


if __name__ == '__main__':
    loop = get_event_loop()
    loop.run_until_complete(main())
    loop.close()
