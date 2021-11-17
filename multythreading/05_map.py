import concurrent.futures

from multythreading.count_three_sum import read_ints, count_three_sum

if __name__ == '__main__':
    print('started main')
    data = read_ints("..\\data\\1Kints.txt")
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        results = executor.map(count_three_sum, (data, data), ('t1', 't2'))  # тут будет х2 вызов: дата+т1, дата+т2
        for r in results:
            print(f'{r=}')  # вывод результата

    print('ended main')
