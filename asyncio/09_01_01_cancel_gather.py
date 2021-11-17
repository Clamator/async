import asyncio
import threading
import time

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
    print(f'{task_name=} sleeping')
    await asyncio.sleep(sleeping_time)
    print(f'{task_name=} woke up')

    await asyncio.sleep(1)
    return [Photo.from_json(photo) for photo in photos_json]


# метод, который возвращает список корутинов
def get_coros(session):
    return [
        photos_by_album('t1', 1, session),
        photos_by_album('t2', 2, session),
        photos_by_album('t3', 3, session),
        photos_by_album('t4', 4, session)
    ]


# мы можем вызывать и на тасках, и на фьючере кэнсел, тут будет на фьючере, хотя это и не рекомендуется
# в этом примере это сработает,в следующем нет
def cancel_future(loop, future, after):
    # тут будет внутренний метод, который будет использован в отдельном потоке
    def inner_cancel():
        print('\nsleeping before future cancel')
        time.sleep(after)  # after - время сна

        print('\ncancel future')
        # непосредственно отмена
        loop.call_soon_threadsafe(future.cancel)

    t = threading.Thread(target=inner_cancel)
    t.start()


def cancel_tasks(tasks, after):
    def inner_cancel():
        time.sleep(after)
        for i, t in enumerate(tasks, start=1):
            print(f'cancel {i} : {t}')
            print(t.cancel())

    t = threading.Thread(target=inner_cancel)
    t.start()


async def main_gather_cancel_of_tasks():  # for CANCEL_TASKS
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(coro) for coro in get_coros(session)]
        future = asyncio.gather(*tasks)
        # отмена фьючер начнем через 2 секунды
        cancel_tasks(tasks, 2)

        try:
            print((f'\nawaiting future'))
            result = await future
        except asyncio.exceptions.CancelledError as ex:
            print(f'exception {repr(ex)}')


async def main_gather_cancel_of_future():  # for CANCEL_FUTURE
    async with aiohttp.ClientSession() as session:
        future = asyncio.gather(*(get_coros(session)))
        # отмена фьючер начнем через 2 секунды
        cancel_future(asyncio.get_running_loop(), future, 2)

        try:
            print((f'\nawaiting future'))
            result = await future
        except asyncio.exceptions.CancelledError as ex:
            print(f'exception {repr(ex)}')


# another method that uses return_exceptions = True
# there should be another output
async def main_gather_return_exceptions():
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(coro) for coro in get_coros(session)]
        future = asyncio.gather(*tasks, return_exceptions=True)

        cancel_tasks(tasks, 2)

        try:
            print(f'\nawaiting future')
            results = await future

            for result in results:
                if isinstance(result, asyncio.exceptions.CancelledError):
                    print(repr(result))
                else:
                    print_photo_titles(results)
            print('after')
        except asyncio.exceptions.CancelledError as ex:
            print(f'Excepted at await {repr(ex)}')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.create_task(main_gather_return_exceptions())
        loop.run_forever()
    finally:
        print('end of work')
        loop.close()
