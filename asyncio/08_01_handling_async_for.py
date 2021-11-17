import asyncio
import time
from typing import List

import aiohttp


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


# метод, который работает с хттпс асинхронно, который будет выкачивать данные по фото из альбома
# как и в библиотеке ресквест тут будет объект session

async def photos_by_album(task_name, album, session) -> List[
    Photo]:  # имя задачи, альбом, который качаем и объект сессии
    print(f'{task_name=}')
    url = f'https://jsonplaceholder.typicode.com/photos?albumId={album}'  # по этой строке делаем запрос,качаем данные

    response = await session.get(url)  # установили сессию
    photos_json = await response.json()  # джейсоним респонс
    await asyncio.sleep(1)
    return [Photo.from_json(photo) for photo in photos_json]


# метод, который позволяет выкачивать список альбомов
async def download_albums(albums):  # получает список айди альбомов
    async with aiohttp.ClientSession() as session:
        for album in albums:
            # тут мы сделали ошибку
            if not isinstance(album, int):
                raise TypeError('INVALID TYPE OF INCOME CODE')
            yield await photos_by_album(f'task - {album}', album, session)


#  мы добавили строку вместо цифры, чтобы можно было заняться обработкой исключений
#  для того, чтобы отлавливать исключения, нам надо заворачивать сам цикл в трай-эксепт
#  после этого код исполняется дальше, до мэйн эндед дошли
async def main():
    try:
        async for photos in download_albums([1, 2, '3', 4]):
            print_photo_titles(photos)
    except Exception as ex:
        print(f'A type error acquired - {ex}, please input only integers')


if __name__ == '__main__':
    asyncio.run(main())

    time.sleep(3)
    print('main ended')
