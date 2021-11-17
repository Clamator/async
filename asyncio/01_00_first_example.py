import asyncio

from multythreading.decorators import async_measure_time


async def tick():  # вызываемая ф-я асинк
    print('tick')
    await asyncio.sleep(1)  # у них и слип есть свой асинх,
    print('tack')


@async_measure_time  # тут мы сделали декоратор
async def main():  # основная ф-я тоже асинк
    await asyncio.gather(tick(), tick(), tick())  # метод всегда с await, gather - типа map


if __name__ == '__main__':
    asyncio.run(main())
