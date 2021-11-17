# синхронно и последовательно выкачиваем контент с сайтов
import asyncio

import aiohttp
import requests

from multythreading.decorators import measure_time, async_measure_time


async def download(url, session):
    async with session.get(url) as response:
        print(f'Read {response.content.total_bytes} from {url}')


@async_measure_time
async def download_all_sites(sites):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in sites:
            task = asyncio.create_task(download(url, session))
            tasks.append(task)

        try:
            print('start')
            await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as ex:
            print(repr(ex))




if __name__ == '__main__':
    sites = [
                'https://www.engineerspock.com/',
            ] * 80
    asyncio.run(download_all_sites(sites))
