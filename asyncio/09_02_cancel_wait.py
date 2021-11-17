import asyncio
from asyncio import FIRST_EXCEPTION

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


async def photos_by_album(task_name, album, session):  # имя задачи, альбом, который качаем и объект сессии
    print(f'{task_name=}')
    if not isinstance(album, int):
        await asyncio.sleep(2)
        raise TypeError(f'INVALID TYPE OF INCOME CODE, album {album} in not available')

    url = f'https://jsonplaceholder.typicode.com/photos?albumId={album}'  # по этой строке делаем запрос,качаем данные

    response = await session.get(url)  # установили сессию
    photos_json = await response.json()  # джейсоним респонс

    # будем делать таски в состоянии слипа
    sleeping_time = 3 if task_name == 't3' else 1
    await asyncio.sleep(sleeping_time)

    print(f'{task_name=} finished task')

    return [Photo.from_json(photo) for photo in photos_json]


async def main_wait():
    async with aiohttp.ClientSession() as session:
        tasks = [
            photos_by_album('t1', 1, session),
            photos_by_album('t2', 2, session),
            photos_by_album('t3', 3, session),
            photos_by_album('t4.0', '4.0', session),
            photos_by_album('t5', 5, session)
        ]

        photos = []
        done_tasks, pending_tasks = await asyncio.wait(tasks, return_when=FIRST_EXCEPTION)
        # ТУТ уже будет выведен f'canselling {pending_task}', вернулось управление, как только мы получили первое искл


        # cancelling the pending tasks
        for pending_task in pending_tasks:
            print(f'canselling {pending_task}')
            print(pending_task.cancel())

        # trying to receive result from the done_tasks
        for done_task in done_tasks:
            try:
                result = done_task.result()
                photos.extend(result)
            except Exception as ex:
                print(repr(ex))

        print_photo_titles(photos)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.create_task(main_wait())
        loop.run_forever()
    finally:
        print('end of main')
        loop.close()
