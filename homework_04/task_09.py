"""
Написать программу, которая скачивает изображения с заданных URL-адресов и сохраняет их на диск.
Каждое изображение должно сохраняться в отдельном файле, название которого соответствует названию изображения в URL-адресе.
Например, URL-адрес: https://example/images/image1.jpg -> файл на диске: image1.jpg
— Программа должна использовать многопоточный, многопроцессорный и асинхронный подходы.
— Программа должна иметь возможность задавать список URL-адресов через аргументы командной строки.
— Программа должна выводить в консоль информацию о времени скачивания каждого изображения.
"""
from asyncio import gather, ensure_future, get_event_loop
from os import path, mkdir
from time import time
from multiprocessing import Process
from threading import Thread
from aiohttp import ClientSession
from requests import get
from sys import argv


def download_image(image_url, folder="."):
    filename = image_url.split('/')[-1]
    with open(path.join(folder, filename), 'wb') as f:
        f.write(get(image_url).content)
    return filename


def sync_download_images(image_urls, folder="."):
    for image in image_urls:
        download_image(image, folder)


def threads_download_image(image_urls, folder="."):
    threads = []
    for image in image_urls:
        thread = Thread(target=download_image, args=(image, folder,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()


def proc_download_image(image_urls, folder="."):
    processes = []
    for image in image_urls:
        process = Process(target=download_image, args=(image, folder,))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()


async def async_download_image(image_url, folder="."):
    async with ClientSession() as session:
        async with session.get(image_url) as response:
            image = await response.read()
            filename = image_url.split('/')[-1]
            with open(path.join(folder, filename), 'wb') as f:
                f.write(image)


async def async_download_images(image_urls, folder="."):
    tasks = []
    for image in image_urls:
        task = ensure_future(async_download_image(image, folder))
        tasks.append(task)
    await gather(*tasks)


if __name__ == '__main__':
    if len(argv) > 1:
        urls = argv[1:]
    else:
        urls = [
            'https://avatanplus.com/files/resources/original/579091ceb27a91560cb98f8b.jpg',
            'https://gas-kvas.com/uploads/posts/2023-02/1675489758_gas-kvas-com-p-izobrazheniya-i-kartinki-na-fonovii-risuno-41.jpg',
            'https://mykaleidoscope.ru/x/uploads/posts/2022-10/1666206241_12-mykaleidoscope-ru-p-kartinka-na-zastavku-oboi-12.jpg',
        ]

    images_path = "images/"

    if not path.exists(images_path):
        mkdir(images_path)

    start_time = time()
    sync_download_images(urls, images_path)
    print(f'Sync time: {time() - start_time:.2f} seconds')

    start_time = time()
    threads_download_image(urls, images_path)
    print(f'Threads time: {time() - start_time:.2f} seconds')

    start_time = time()
    proc_download_image(urls, images_path)
    print(f'Processes time: {time() - start_time:.2f} seconds')

    start_time = time()
    loop = get_event_loop()
    loop.run_until_complete(async_download_images(urls, images_path))
    loop.close()
    print(f'Async time: {time() - start_time:.2f} seconds')
