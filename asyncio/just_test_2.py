import asyncio


async def printing():
    print(123)
    await asyncio.sleep(0)
    print(3343)


async def printing2():
    print(334)
    await asyncio.sleep(0)
    print(1232)


ioloop = asyncio.get_event_loop()
tasks = [ioloop.create_task(printing()), ioloop.create_task(printing2())]
wait_tasks = asyncio.wait(tasks)
ioloop.run_until_complete(wait_tasks)
ioloop.close()
