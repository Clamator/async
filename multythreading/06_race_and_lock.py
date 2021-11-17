import concurrent.futures
import threading
import time


class BankAccount:
    def __init__(self):
        self.balance = 100  # тот ресурс, котоый будет использован потоками
        self.lock_obj = threading.Lock()  # тут мы ничего не захватываем
    def update(self, transaction, amount):
        print(f'{transaction} started')

        with self.lock_obj:  # и вот эта тема уже решает проблему, он захватывает один поток, а другой уже ждет
            tmp_balance = self.balance
            tmp_balance += amount
            time.sleep(1)  # вызывает переключение контекста
            self.balance = tmp_balance

        print(f'\n{transaction} ended')


if __name__ == '__main__':


    acc = BankAccount()
    print(f'main started, acc balance = {acc.balance}')
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        ex.map(acc.update, ('refill', 'withdraw'), (100, -190))
    print(f'end of main, balance = {acc.balance}')
