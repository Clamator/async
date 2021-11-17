import concurrent.futures
import threading
import time


def div(divisor, limit):
    print(f'started div {divisor}')

    result = 0
    for x in range(1, limit):
        if x % divisor == 0:
            print(f'divisor= {divisor}, x= {x}')
            result += x
        time.sleep(0.2)

    print('exception is raised')
    raise Exception('smth went wrong')


if __name__ == '__main__':
    print('started main')

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        res_list = ex.map(div, (3, 15), (4, 24))
        while res_list:
            try:
                cur_list = next(res_list)
            except StopIteration:
                print('stop iteration #1')
                break
            except Exception as ex:
                print(repr(ex), 'unhandled error')

    print('main ended')

# if __name__ == '__main__':
#    print('main started')
#
#    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
#        future = ex.submit(div, 3, 25)
#        time.sleep(3)
#        try:
#            res = future.result()
#        except Exception as ex:
#            print(repr(ex))
#    print('main ended')
#
