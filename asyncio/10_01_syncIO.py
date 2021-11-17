# синхронно и последовательно выкачиваем контент с сайтов

import requests

from multythreading.decorators import measure_time


def download(url, session):
    with session.get(url) as response:
        print(f'Read {len(response.content)} from {url}')


@measure_time
def download_all_sites(sites):
    with requests.Session() as session:
        for url in sites:
            download(url, session)


if __name__ == '__main__':
    sites = [
                'https://www.engineerspock.com/',
            ] * 80
    download_all_sites(sites)
