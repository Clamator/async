# будет два потока - один подключается, втрой выставляет флажок, исчерпана ли емкость семафора
import concurrent.futures
import threading
import time


def work(semaphore):
    time.sleep(8)
    print('releasing one connection')
    semaphore.release()


def connect(semaphore, reached_max_connections):
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
        # тут будем эмулировать подключения к базе данных
        while True:
            connections_counter = 0
            while not reached_max_connections.is_set():
                print(f'connection # = {connections_counter}')
                semaphore.acquire()
                connections_counter += 1

                ex.submit(work, semaphore)
                time.sleep(0.8)

            time.sleep(5)


def connection_guard(semaphore, reached_max_connections):
    while True:
        print(f'[guard] semaphore = {semaphore._value}')
        time.sleep(1.5)  # слипы нужны для того, чтобы код успел реагировать на изменения

        if semaphore._value == 0:  # если 0 - доступных слотов(подключений) нет
            reached_max_connections.set()  # этот метод будет сигнализировать, что мы достигли максимум подключений
            print('[guard] reached max connections')
            time.sleep(2)  # чтобы другой поток успел увидеть флаг
            reached_max_connections.clear()


if __name__ == '__main__':  # более высокий уровень
    max_connections = 10
    reached_max_connections = threading.Event()  # для сигнализации, что достигнуто мак кол-во

    semaphore = threading.Semaphore(value=max_connections)
    # сейчас сделаем как раз таки две функции, и там у каждой будет свой поток
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(connection_guard, semaphore, reached_max_connections)  # следит за исчерпанием емкости
        executor.submit(connect, semaphore, reached_max_connections)  # эта коннетится
