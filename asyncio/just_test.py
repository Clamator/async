import asyncio
import time

lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]


async def printing(lst):
    for el in lst:
        if el % 2 == 0:
            print(f'{el} is ok')
            time.sleep(1)
    return 'abc'

async def printing2(lst):
    for el in lst:
        if el % 2 != 0:
            print(f'{el} is not ok')
            time.sleep(1)
    return 'xyz'

async def main():
    t1 = asyncio.create_task(printing(lst))
    t2 = asyncio.create_task(printing2(lst))

    for t in asyncio.as_completed((t1, t2)):
        result = await t
        print(result)



if __name__ == '__main__':
    asyncio.run(main())