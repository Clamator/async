import threading
import time

a = 5
b = 5

a_lock = threading.Lock()
b_lock = threading.Lock()


def thread1calc():
    global a
    global b

    print('thread1 acquires a')
    a_lock.acquire()
    time.sleep(2)

    print('thread1 acquires b')
    b_lock.acquire()
    time.sleep(2)

    a += 5
    b += 5

    print('thread1 releases both locks')
    a_lock.release()
    b_lock.release()


def thread2calc():
    global a
    global b

    print('thread2 acquires b')
    b_lock.acquire()
    time.sleep(2)

    print('thread2 acquires a')
    a_lock.acquire()
    time.sleep(2)

    a += 10
    b += 10

    print('thread2 releases both locks')
    b_lock.release()
    a_lock.release()

if __name__ == '__main__':
    t1 = threading.Thread(target=thread1calc)
    t1.start()
    t2 = threading.Thread(target=thread2calc)
    t2.start()