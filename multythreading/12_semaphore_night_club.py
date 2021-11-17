import threading
import time


class NightClub:
    def __init__(self):
        self.bouncer = threading.Semaphore(3)  # прям в конструкторе инициализируем семафор с тремя персами одновременно

    # будет два метода: один в цикле запускает потоки, а потоки будут таргетировать другой метод
    # который будет захватывать наш семафор, спать, а затем отпускать семафор
    def open_club(self):
        for x in range(1, 11):
            t = threading.Thread(target=self.guest, args=[x])  # тут будет ф-я и текущ состояние икса
            t.start()

    def guest(self, guest_id):
        print(f'\nGuest {guest_id} is waiting to enter in night club')
        self.bouncer.acquire()  # захват семафора, типа вход в клуб
        print(f'\nGuest {guest_id} is dancing')
        time.sleep(2)
        print(f'\nGuest {guest_id} is leaving the club')
        self.bouncer.release()


if __name__ == '__main__':
    club = NightClub()
    club.open_club()
