"""
Создать программу, которая будет производить подсчет
количества слов в каждом файле в указанной директории и
выводить результаты в консоль.
Используйте процессы.
"""

from multiprocessing import Process

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
        if os.path.isfile(os.path.join(path, file)):
            files.append(os.path.join(path, file))
    return files


if __name__ == '__main__':
    processes = []
    for filename in dir_files('.'):
        process = Process(target=count_words, args=[filename])
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
