import concurrent.futures
import time


def div(divisor, limit):
    print(f'started div {divisor}')

    result = 0
    for x in range(1, limit):
        if x % divisor == 0:
            # print(f'divisor= {divisor}, x= {x}')
            result += x
        time.sleep(0.2)

    return result


if __name__ == '__main__':
    print('started main')
    futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures.append(executor.submit(div, 3, 25))  # т.к. сабмит возв-ет фьючерс, мы его можем доб в пер-ную
        futures.append(executor.submit(div, 5, 25))
        print('\nimmediately printed out after sumbit')
        while futures[0].running() and futures[1].running():  # пока 0 и 1 элты в активном статусе, выводить точку
            print('.', end='')
            time.sleep(1)

        for f in futures:  # выводим возвращаемый результат
            print(f'\n{f.result()}')

    print('after "with" block')
