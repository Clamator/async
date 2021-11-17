import multiprocessing
import time

from multythreading.count_three_sum import read_ints, count_three_sum

if __name__ == '__main__':
    print('\nStarted main')
    ints = read_ints("..\\data\\1Kints.txt")
    # процесс будет идти именно в процессе, типа поток в процессе

    p = multiprocessing.Process(target=count_three_sum, args=(ints,))
    p.start()  # процесс.старт
    time.sleep(5)

    p.terminate()

    print('end of main. process was terminated')
