import threading
import time

from multythreading.count_three_sum import read_ints

should_stop = False  # это и есть флаг




def count_three_sum(ints, thread_name='t'):
    print(f'started count_three_sum in {thread_name}')
    n = len(ints)

    counter = 0

    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if should_stop:
                    print('\ntask was canceled')
                    counter = -1  # типа договорились, чт такое знаение будет присваиваться
                    return  counter  # выход из цикла, если делать брейк, то надо из трех циклов выходить
                if ints[i] + ints[j] + ints[k] == 0:
                    counter += 1
                    print(f"triple found in {thread_name}: {ints[i]}, {ints[j]}, {ints[k]}", end="\n")  # можно убрать эту строчку

    print(f'finished count_three_sum in {thread_name}. Triplets amount is {counter}')
    return counter

if __name__ == '__main__':
    print('\nStarted main')
    ints = read_ints("..\\data\\1Kints.txt")
    # процесс будет идти именно в процессе, типа поток в процессе

    p = threading.Thread(target=count_three_sum, args=(ints,))
    p.start()  # процесс.старт
    time.sleep(5)

    should_stop = True

    print('end of main. process was terminated')