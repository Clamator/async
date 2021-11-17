import asyncio


async def tick():
    print('tick')
    await asyncio.sleep(1)
    print('tack')
    await asyncio.sleep(1)
    return "tick-tack"

async def main():
    t1 = asyncio.create_task(tick(), name='Tick1')
    t2 = asyncio.ensure_future(tick())  # тут имя уже нельзя прописать
    results = await asyncio.gather(t1, t2)
    for _ in results:
        print(_)

    print(f'Task {t1.get_name()}. Done = {t1.done()}')
    print(f'Task {t2.get_name()}. Done = {t2.done()}')

if __name__ == '__main__':
    asyncio.run(main())
