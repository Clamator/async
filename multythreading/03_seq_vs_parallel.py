import threading

from multythreading.count_three_sum import read_ints, count_three_sum
from multythreading.decorators import measure_time


@measure_time
def run_par(ints):
    t1 = threading.Thread(target=count_three_sum, daemon=True, args=(ints, 't1'))  # второе т1 это типа имя потока?
    t2 = threading.Thread(target=count_three_sum, daemon=True, args=(ints, 't2'))

    t1.start()
    t2.start()

    print('\nPlease, wait for threads to over')

    t1.join()  # не даем завершиться ф-и
    t2.join()


@measure_time
def run_seq(ints):
    count_three_sum(ints, 'main')
    count_three_sum(ints, 'main2')


if __name__ == '__main__':
    print('started main')
    ints = read_ints("..\\data\\1Kints.txt")
    run_par(ints)
    run_seq(ints)

    print('all done')
