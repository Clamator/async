import asyncio
# тут  у нас уже будет две ф-и
import time


async def tick():
    await asyncio.sleep(1)
    return "tick"


async def tack():
    await asyncio.sleep(2)
    return "tack"


async def main():
    start = time.perf_counter()
    t1 = asyncio.create_task(tick())
    t2 = asyncio.create_task(tack())

    for i, t in enumerate(asyncio.as_completed((t1, t2)), start=1):
        result = await t
        elapsed = time.perf_counter() - start
        print(f'num={i} elapsed in {elapsed:0.2f} seconds')
        print(result)


if __name__ == '__main__':

    asyncio.run(main())
    print("all done")
