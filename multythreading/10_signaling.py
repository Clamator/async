import random
import threading
import time
from enum import Enum


#  все, что ниже, это, допустим граница приложения, на которую мы почти или никак не влияем, сверху будет клиентская


# все, что ниже, это, допустим граница приложения, на которую мы почти или никак не влияем, сверху будет клиентская

class Event:  # это не примитив, просто класс, он не стопарит исполнение потока
    def __init__(self):
        self.__handlers = []

    def __call__(self, *args, **kwargs):  # объекты будут вызываемыми
        for f in self.__handlers:  # когда мы вызываем ивент, надо дернуть всех подписчиков
            f(*args, **kwargs)  # передаем в каждого подписчика элементы

    def __iadd__(self, handler):  # для более удобного подписывания +=
        self.__handlers.append(handler)
        return self  # обязательно

    def __isub__(self, handler):  # эта ф-я для отписывания -=
        self.__handlers.remove(handler)
        return self


class OperationStatus(Enum):
    FINISHED = 0
    FAULTED = 1


class Protocol:  # некий протокол взаимодействия

    def __init__(self, port, ip_address):  # порт и адрес, по которому библиотека будет подключаться к терминалу банка
        self.port = port
        self.ip_address = ip_address
        self.set_ip_port()  # эмулируем запрос на получение порта тут

        #  класс протокол создает ивент, потому что протокол будет получать ответ от third-party библиотеки
        #  также будет происходить оповещение всех подписантов, что событие совершилось
        #  тот, кто будет пользоваться классом протокол, сможет подписаться на этот ивент
        self.message_received = Event()  # тут как раз и происходит оповещение

    def set_ip_port(self):
        # тут будет происходить якобы получение ипа и порта, всего это делается один раз
        print('set ip and port once')
        time.sleep(0.2)
        return

    def send(self, op_code, param):  # ф-я отправляет в библиотеку коды операции, какие-то параметры
        def process_sending():  # именно она будет отправлять в биб-ку сообщ и возбужд сообщ после получ рез-та
            print(f'operation is in action with param = {param}')
            result = self.process(op_code, param)  # имитация взаимодействия с библиотекой
            self.message_received(result)  # вызов, чтобы уведомить подписантов, что событие произошло, передача рез-та
            # когда мы вызываем эту ф-ю, вызываются все подписанты события

        t = threading.Thread(target=process_sending)
        t.start()

    def process(self, op_code, param):
        print(f'started operation with {op_code}, param = {param}')  # эмуляция работы
        time.sleep(3)  # эмуляция, типа там что-то работает

        # тут будет типа ответ библиотеки
        finished = random.randint(0, 1) == 0
        return OperationStatus.FINISHED if finished else OperationStatus.FAULTED


class BankTerminal:
    def __init__(self, port, ip_address):
        self.ip_address = ip_address
        self.port = port
        self.protocol = Protocol(port, ip_address)
        self.protocol.message_received += self.on_message_received  # o_m_r - это подписант
        # Event - это примитив, а не класс
        self.operation_signal = threading.Event()  # это и есть примитив синхронизации

    def on_message_received(self, status):  # ф-я обрабатывает событие
        # отпускаем метод тут, ибо знаем,что операция завершена
        print(f'signaling for an event: {status}')
        self.operation_signal.set()  # сигнал, типа хватит ждать

    #  реализуем ф-ю покупки, и чтобы верхний уровень мог дождаться завершения операции
    def purchase(self, amount):  # инициация покупки, передается цена, дб асинхронным
        def process_purchase():
            purchase_op_code = 1  # код операции
            self.protocol.send(purchase_op_code, amount)
            # нам надо дождаться завершения операции,
            # для этого создаем примитив синхронизации self.operation_signal = threading.Event
            self.operation_signal.clear()  # когда вызывается сет, Event переходит в состояние "просигналено",
            # поэтому метод clear нужен для очистки этого статуса, чтобы потом еще раз делать wait
            print('\nWaiting for a signal')
            self.operation_signal.wait()
            print('purchase finished')

        t = threading.Thread(target=process_purchase)
        t.start()

        return t


if __name__ == "__main__":
    bt = BankTerminal(1090, '100.100.0.0')
    t = bt.purchase(20)
    print('Main decided to wait for purchase 1')
    t.join()
    t = bt.purchase(30)
    print('Main decided to wait for purchase 2')
    t.join()

    print('end of main')
