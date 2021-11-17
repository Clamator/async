import threading
import time

throw = False


def count():
    i = 0
    try:
        while True:
            if throw:
                raise ArithmeticError()

            i += 1
            print(f'{i=}')
            time.sleep(1)
    except ArithmeticError:
        print('en error occurred')


if __name__ == '__main__':
    print('main started')

    t = threading.Thread(target=count)
    t.start()

    time.sleep(5)
    throw = True
    for y in range(1, 10):
        print(f'{y=}')
        time.sleep(1)

