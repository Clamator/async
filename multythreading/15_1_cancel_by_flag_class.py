import threading
import time

from multythreading.count_three_sum import read_ints


class ThreeSumTask:
    def __init__(self, ints):
        self.ints = ints
        self.canceled = False
        self.lock_obj = threading.Lock()

    def run(self):
        self.count_three_sum(self.ints)

    def cancel(self):
        with self.lock_obj:
            self.canceled = True

    def count_three_sum(self, ints):
        print(f'started count_three_sum')
        n = len(ints)

        counter = 0

        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    if self.canceled:
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

    task = ThreeSumTask(ints)

    t1 = threading.Thread(target=task.run)
    t1.start()  # процесс.старт
    time.sleep(5)
    task.cancel()  # проставляет отмену в тру
    t1.join()
    print('end of main. process was terminated')
