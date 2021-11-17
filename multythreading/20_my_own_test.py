import threading
import time


class Telephone:
    def __init__(self):
        self.update = threading.Event()

    def turn_on(self):
        print('\ntelephone is turning on')
        for x in range(10):
            print('.', end=' ')
            time.sleep(1)
            self.update.clear()

    def updating(self):
        print('\ntelephone is updating')
        time.sleep(1)
        for x in range(15):
            print('.', end=' ')
            time.sleep(1)
        self.update.set()
        if self.update.is_set():
            self.turn_on()
            print('\ntelephone is successfully updated')


if __name__ == '__main__':
    tp = Telephone()
    tp.updating()
