import threading
import time

from multythreading.count_three_sum import read_ints


class StoppableThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self.stop_event = threading.Event()  # для сигнала используем ивент

    def stop(self):
        self.stop_event.set()

    def stopped(self):
        return self.stop_event.is_set()


class ThreeSumUnitOfWork(StoppableThread):  # тут происходит наследование от треда

    def __init__(self, ints, name="ThreadTest"):
        super().__init__(name=name)
        self.ints = ints
        # self.stop_event = threading.Event()  # для сигнала используем ивент

    def run(self):
        print(f'thread {self.getName()} starts')  # гет нейм - получить имя и все
        self.count_three_sum(self.ints)
        print(f'thread {self.getName()} ends')

    def stop(self):
        self.stop_event.set()  # оповещение, что флаг отработал

    def count_three_sum(self, ints):
        print(f'started count_three_sum')
        n = len(ints)

        counter = 0

        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    if super().stopped():  # проверка, сработал ли флаг?, обращение через более высокий класс
                        print('\ntask was canceled')
                        counter = -1  # типа договорились, чт такое знаение будет присваиваться
                        return counter  # выход из цикла, если делать брейк, то надо из трех циклов выходить
                    if ints[i] + ints[j] + ints[k] == 0:
                        counter += 1
                        print(f"triple found: {ints[i]}, {ints[j]}, {ints[k]}",
                              end="\n")  # можно убрать эту строчку

        print(f'finished count_three_sum in. Triplets amount is {counter}')
        return counter


if __name__ == '__main__':
    print('\nStarted main')
    ints = read_ints("..\\data\\1Kints.txt")

    task = ThreeSumUnitOfWork(ints)

    # t1 = threading.Thread(target=task.run)
    task.start()  # процесс.старт, класс наследуется от треда, поэтому в него уже зашит таргет с таск.ран
    time.sleep(5)
    task.stop()  # проставляет отмену в тру

    task.join()
    print(task.stopped())
    print('end of main. process was terminated')

# по сути был создан объект, который явлется задачей, и мы им манипулируем как тредом
