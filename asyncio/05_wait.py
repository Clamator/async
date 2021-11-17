#  будем обращаться к сервисам, которые определяют текущий ип адрес
import asyncio
from asyncio import FIRST_COMPLETED
from collections import namedtuple

import aiohttp

Service = namedtuple('Service', ('name', 'url', 'ip_attr'))
services = (
    Service('ipify', 'https://api.ipify.org?format=json', 'ip'),
    Service('ip-api', 'http://ip-api.com/json', 'query')
)


async def get_json(url):
    async with aiohttp.ClientSession() as session:  # типа именование сессии,
        async with session.get(url) as response:  # а тут уже установка самой сессии
            return await response.json()


#  метод, которым мы будем вытаскивать айпи из этого джейсона
async def fetch_ip(service):
    print(f"fetching IP from {service.name}")

    json_response = await get_json(service.url)
    ip = json_response[service.ip_attr]
    return f"{service.name} has finished with result: {ip}"


async def main():
    # создаем через ЛК список корутинов
    coros = [fetch_ip(service) for service in services]
    done, pending = await asyncio.wait(coros, return_when=FIRST_COMPLETED)
    # создаем два кортежа с заверш и ожид, уйэт возвр-т фьючеры
    # FIRST_COMPLETED - это флажок, тут видим, что второй рез-т не был получен, после получения ост таски отменяются
    # даже если они и работают, то резта мы от них не увидим

    # тут таски, которые являются сами по себе фьючерами, только более высокоуровневые
    for x in done:
        print(x.result())

if __name__ == '__main__':
    asyncio.run(main())
