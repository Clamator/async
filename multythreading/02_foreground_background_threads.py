import threading


from multythreading.count_three_sum import read_ints, count_three_sum

if __name__ == '__main__':
    print('started main')

    ints = read_ints("..\\data\\1Kints.txt")  # тут мы сначала делаем список чисел, записывая их в интс

    t1 = threading.Thread(target=count_three_sum, daemon=True, kwargs=dict(ints=ints))

    t1.start()  # старт потока
    name = input('\nWhat is your name?')
    print(f'Hello, {name}. Please, wait until the counting overs')
    t1.join()
    print('all done')

# а тут мы вызвали ф-ю слип, которая дала потоку немного поработать, а после он обрубился
# но в чем проблема, т.к. оба потока делали принт в консоли, вывести имя и список триплетов правильно не получается