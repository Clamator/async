# здесь будет оптимизация - будем использовать локальное хранилище для потоков
# у нас будет 5 потоков, чтобы каждый раз один и тот же тред не пересоздавать сессион, мы и используем ЛХДП
# один раз будет создан сессион и больше не будет
import concurrent.futures
import threading

import requests

from multythreading.decorators import measure_time

# и есть этот самый ЛХДП
thread_local = threading.local()


# в этот метод заходит поток, он проверяет, есть ли атрибут сессия в тред_локал, если нет - создает и возвращает
# если есть, то просто возвращает имеющийся
def get_session():
    if not hasattr(thread_local, 'session'):
        thread_local.session = requests.Session()
    return thread_local.session


def download(url):
    session = get_session()

    with session.get(url) as response:
        print(f'Read {len(response.content)} from {url}')


@measure_time
def download_all_sites(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(download, sites)


if __name__ == '__main__':
    sites = [
                'https://www.engineerspock.com/',
            ] * 80
    download_all_sites(sites)
