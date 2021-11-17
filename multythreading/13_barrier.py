import datetime
import random
import threading
import time


class HorseRace:
    def __init__(self):
        self.barrier = threading.Barrier(4)
        self.horses = ['horse1', 'horse2', 'horse3', 'horse4']

    def lead(self):
        horse = self.horses.pop()
        time.sleep(random.randint(1, 5))
        print(f'\nthe {horse} has reached the barrier at {datetime.datetime.now()}')
        self.barrier.wait()

        time.sleep(random.randint(1, 5))
        print(f'\nthe {horse} started the race at {datetime.datetime.now()}')
        # self.barrier.wait()

        time.sleep(random.randint(1, 5))
        print(f'\nthe {horse} finished at {datetime.datetime.now()}')

        self.barrier.wait()
        print(f'\nthe {horse} went to sleep')


if __name__ == '__main__':
    # threads = []
    print('\nRace preparation')

    race = HorseRace()
    for x in range(4):
        thread = threading.Thread(target=race.lead)
        thread.start()


