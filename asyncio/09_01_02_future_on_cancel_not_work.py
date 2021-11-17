# демонстрация проблемы отмены через фьючер
import asyncio


class ErrorThatShouldCancelOtherTasks(Exception):
    pass


async def my_sleep(secs):  # income random number of secs
    print(f'task {secs}')
    await asyncio.sleep(secs)
    print(f'task {secs} finished sleeping')

    if secs == 5:
        raise ErrorThatShouldCancelOtherTasks('5 if forbidden')  # catch and cancelling tasks from outer space
    print(f'slept for {secs} secs')


async def main_cancel_tasks():
    tasks = [asyncio.create_task(my_sleep(secs)) for secs in [2, 5, 7]]
    sleepers = asyncio.gather(*tasks)  # sleeper is a FUTURE
    print('awaiting')
    try:
        await sleepers
    except ErrorThatShouldCancelOtherTasks:
        print('cancelling...')
        for t in tasks:
            print(f'cancelling {t}')
            print(t.cancel())
    finally:
        await asyncio.sleep(5)


# main method that works and cancel evth
async def main_cancel_future():
    sleepers = asyncio.gather(*[my_sleep(secs) for secs in [2, 5, 7]])  # sleeper is a FUTURE
    print('awaiting')
    try:
        await sleepers
    except ErrorThatShouldCancelOtherTasks:
        print('cancelling...')
        sleepers.cancel()
    finally:
        await asyncio.sleep(5)


if __name__ == '__main__':
    asyncio.run(main_cancel_tasks())

# two tasks has not been cancelled because of a DONE statement, the third task wan cancelled and we can see True
# so we must not to make cancelling with FUTURE
