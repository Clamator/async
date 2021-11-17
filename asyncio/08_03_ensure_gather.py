import asyncio
import time
from typing import List

import aiohttp


#  когда мы просматриваем результат из колбэка, навешенного на таск, и если там вылетает исключение и мы его не
# обрабатываем, оно не убивает приложение, но если мы делает await на таске,все работает как обычно

class Photo:
    def __init__(self, album_id, photo_id, title, url, thumbnail_url):
        self.thumbnail_url = thumbnail_url
        self.url = url
        self.title = title
        self.photo_id = photo_id
        self.album_id = album_id

    # классметод, который парсит кусок джейсона и возвращает объект фотографии
    @classmethod
    def from_json(cls, obj):
        return Photo(obj['albumId'], obj['id'], obj['title'], obj['url'], obj['thumbnailUrl'])


# метод, который выводит титульники фотографий
def print_photo_titles(photos):
    for photo in photos:
        print(f'{photo.title}', end='\n')


async def photos_by_album(task_name, album, session) -> List[
    Photo]:  # имя задачи, альбом, который качаем и объект сессии
    # теперь мы тут сделали ошибку

    print(f'{task_name=}')
    if not isinstance(album, int):
        await asyncio.sleep(2)
        raise TypeError(f'INVALID TYPE OF INCOME CODE, album {album} in not available')
    url = f'https://jsonplaceholder.typicode.com/photos?albumId={album}'  # по этой строке делаем запрос,качаем данные

    response = await session.get(url)  # установили сессию
    photos_json = await response.json()  # джейсоним респонс

    await asyncio.sleep(1)
    return [Photo.from_json(photo) for photo in photos_json]


async def download_albums(albums):  # получает список айди альбомов
    photos = []
    async with aiohttp.ClientSession() as session:
        for album in albums:
            photos.extend(await photos_by_album(f'task - {album}', album, session))
    return photos


# 4 альбом не был использован
async def main1():
    task1 = asyncio.create_task(download_albums([1, 2, '3', 4]))
    try:
        result = await task1  # это не колбэк, а await, колбэк - это ф-я
    except Exception as ex:
        print(repr(ex))
    print('sleeping in main')
    await asyncio.sleep(1)
    print('after sleep printing')


def handle_result(fut):  # в ф-ю приходит фьючер
    print(fut.result())  # т.к. нет обработки, приложение должно отвалиться, но нет


async def main2():
    task1 = asyncio.create_task(download_albums([1, 2, '3', 4]))
    task1.add_done_callback(handle_result)  # значит, этот возвращает фьючер

    print('sleeping in main')
    await asyncio.sleep(1)
    print('after sleep printing')


async def main_gather():
    # здесь мы конструируем список тасков, которые мы будем запускать,
    async with aiohttp.ClientSession() as session:
        tasks = [
            photos_by_album('t1', 1, session),
            photos_by_album('t2', 2, session),
            photos_by_album('t3', '3', session),
            photos_by_album('t4', 4, session)
        ]
        photos = []
        results = await asyncio.gather(*tasks, return_exceptions=True)  # позволяет вернуть резт из норм ф-й
        for res in results:
            if isinstance(res, Exception):
                print(repr(res))
            else:
                photos.extend(res)

        print_photo_titles(photos)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.create_task(main_gather())
        loop.run_forever()
    finally:
        print('main ended')
        loop.close()
