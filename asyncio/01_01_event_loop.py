import asyncio




async def tick():  # вызываемая ф-я асинк
    print('tick')
    await asyncio.sleep(1)  # у них и слип есть свой асинх,
    print('tack')
    loop2 = asyncio.get_running_loop()
    if loop2.is_running():
        print('loop is running')

async def main():  # основная ф-я тоже асинк
    await asyncio.gather(tick(), tick(), tick())  # метод всегда с await, gather - типа map


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.create_task(main())  # блокирующий вызов
        loop.run_forever()
        print('coroutines have finished')
    except KeyboardInterrupt:
        print('app was closed manually')
    finally:
        loop.close()
        print('loop has been closed')

