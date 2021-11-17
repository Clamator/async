import asyncio
import threading
import time


class Terminal:

    async def start(self):
        #  тут мы сами будем создавать заглушку фьюче
        #  тут мы породили фьюче, из любой синхронной ф-и можно вызвать асинхронную, создав ивентлуп
        loop = asyncio.get_event_loop()  # можно гет_ранинг_луп(), здесь мы нашли ивентлуп
        future = loop.create_future()  # создали заглушку фьюче,в который будет записываться результат
        t = threading.Thread(target=self.run_cmd, args=(loop, future,))  # делается все тут, арги переданы
        t.start()
        return await future

    # этот метод будет запущен  в отдельном потоке и должен будет установить результат вызова метода старт
    def run_cmd(self, loop, future):
        # здесь делается колбэк - результат устанавливается не в том потоке, в котором порожден луп и фьюче
        time.sleep(1)
        loop.call_soon_threadsafe(future.set_result, 1)  # именно это и устанавливает результат


async def main():
    t = Terminal()
    result = await t.start()  # метод класса
    print(result)


if __name__ == '__main__':
    asyncio.run(main())  # значит, тут мы создаем ивентлуп?
