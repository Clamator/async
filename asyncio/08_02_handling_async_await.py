import asyncio
import time
from typing import List

import aiohttp


#  когда мы просматриваем результат из колбэка, навешенного на таск, и если там вылетает исключение и мы его не


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
    #
    if not isinstance(album, int):
        raise TypeError(f'INVALID TYPE OF INCOME CODE, album {album} in not available')
    print(f'{task_name=}')
    url = f'https://jsonplaceholder.typicode.com/photos?albumId={album}'  # по этой строке делаем запрос,качаем данные

    response = await session.get(url)  # установили сессию
    photos_json = await response.json()  # джейсоним респонс

    await asyncio.sleep(1)
    return [Photo.from_json(photo) for photo in photos_json]


async def download_albums(albums):  # получает список айди альбомов
    async with aiohttp.ClientSession() as session:
        for album in albums:
            # тут уже идет отлов ошибок, причем он дал закончить также и четвертому альбому отработать
            try:
                yield await photos_by_album(f'task - {album}', album, session)
            except Exception as ex:
                print(repr(ex))


async def main():
    # try: ПРИ ОБРАБОТКЕ ИСКЛЮЧЕНИЯ ЗДЕСЬ МЫ БЫ НЕ ДОШЛИ ДО 4
    async for photos in download_albums([1, 2, '3', 4]):  # здесь также строка вместо цифры
        print_photo_titles(photos)
    # except Exception as ex:
    #    print(f'A type error acquired - {ex}, please input integers only')


if __name__ == '__main__':
    asyncio.run(main())

    time.sleep(3)

    print('main ended')
