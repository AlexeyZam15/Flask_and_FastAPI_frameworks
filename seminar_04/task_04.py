"""
Создать программу, которая будет производить подсчет
количества слов в каждом файле в указанной директории и
выводить результаты в консоль.
Используйте потоки.
"""

from threading import Thread

import os


def count_words(filename):
    with open(filename, 'r', encoding="utf-8") as file:
        text = file.read()
        words = text.split()
        print(f"Файл {filename} содержит {len(words)} слов")


def dir_files(path='.'):
    """Возвращает список файлов в текущей директории"""
    files = []
    for file in os.listdir(path):
        if os.path.isfile(file):
            files.append(file)
    return files


if __name__ == '__main__':
    threads = []
    for filename in dir_files():
        thread = Thread(target=count_words, args=[filename])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
