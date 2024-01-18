"""
Создать программу, которая будет производить подсчет
количества слов в каждом файле в указанной директории и
выводить результаты в консоль.
Используйте асинхронный подход
"""

import asyncio
import os

counter = 0


async def count_words(filename):
    global counter
    counter += 1
    with open(filename, 'r', encoding="utf-8") as file:
        text = file.read()
        words = text.split()
        print(f"Файл {filename} содержит {len(words)} слов")


def dir_files(path='.'):
    """Возвращает список файлов в текущей директории"""
    files = []
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            files.append(os.path.join(path, file))
    return files


async def process_directory(path):
    files = dir_files(path)
    tasks = [asyncio.create_task(count_words(f)) for f in files]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    dir_path = "."
    asyncio.run(process_directory(dir_path))
