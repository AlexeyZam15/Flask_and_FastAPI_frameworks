"""
Напишите программу на Python, которая будет находить
сумму элементов массива из 1000000 целых чисел.
Пример массива: arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...]
Массив должен быть заполнен случайными целыми числами
от 1 до 100.
При решении задачи нужно использовать многопоточность, многопроцессорность и асинхронность.
В каждом решении нужно вывести время выполнения
вычислений.
"""
from random import randint
from multiprocessing import Process, Value
from threading import Thread
from asyncio import gather, run, create_task

from time import time


def create_random_array(size):
    return [randint(1, 100) for _ in range(size)]


def sum_array(array):
    return sum(array)


def th_sum_array(array):
    global th_sum
    th_sum += sum(array)


def threads_sum_array(array, threads_count):
    threads = [Thread(target=th_sum_array, args=(array[i::threads_count],))
               for i in range(threads_count)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return th_sum


def pr_sum_array(array, cnt):
    with cnt.get_lock():
        cnt.value += sum(array)


def processes_sum_array(array, proc_count):
    result = Value('i', 0)
    processes = [Process(target=pr_sum_array, args=(array[i::proc_count], result))
                 for i in range(proc_count)]
    for process in processes:
        process.start()
    for process in processes:
        process.join()
    return result.value


async def as_sum_array(array):
    return sum(array)


async def async_sum_array(array, tasks_count):
    tasks = [create_task(as_sum_array(array[i::tasks_count])) for i in range(tasks_count)]
    result = await gather(*tasks)
    return sum(result)


if __name__ == '__main__':
    array_size = 10000000
    array = create_random_array(array_size)
    start_time = time()
    result = sum_array(array)
    print(f"Synchronous: {time() - start_time:.2f} seconds")
    print(result)

    start_time = time()
    th_sum = 0
    threads_sum_array(array, 10)
    print(f"Threads: {time() - start_time:.2f} seconds")
    print(th_sum)

    start_time = time()
    result = processes_sum_array(array, 10)
    print(f"Processes: {time() - start_time:.2f} seconds")
    print(result)

    start_time = time()
    result = run(async_sum_array(array, 10))
    print(f"Async: {time() - start_time:.2f} seconds")
    print(result)
