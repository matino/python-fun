from threading import Thread, BoundedSemaphore, Lock
from random import randint
from time import sleep

NUM = 3


class Fork(object):
    def __init__(self, id):
        self.lock = Lock()
        self.id = id

    def grab(self, id):
        self.lock.acquire()
        print "Fork# %d was grabbed by philosopher# %d" % (self.id, id)

    def lay_down(self, id):
        print "Fork# %d was layed down by philosopher# %d" % (self.id, id)
        self.lock.release()

    def __str__(self):
        return "Fork# %d" % self.id


class Philosopher(Thread):
    def __init__(self, id, left, right, sem=None, *args, **kwargs):
        super(Philosopher, self).__init__(*args, **kwargs)
        self.id = id
        self.left = left
        self.right = right
        self.semaphore = sem

    def run(self):
        while True:
            self._think()
            self._eat()

    def _think(self):
        print "Philosopher# %d is thinking" % self.id
        sleep(randint(3, 5))

    def _eat(self):
        print "Philosopher# %d is hungry" % self.id

        self.semaphore.acquire()
        self.left.grab(self.id)
        sleep(3)
        self.right.grab(self.id)

        print "Philosopher# %d is eating" % self.id

        sleep(randint(1, 3))
        self.left.lay_down(self.id)
        self.right.lay_down(self.id)

        print "Philosopher# %d finished eating" % self.id

        self.semaphore.release()


if __name__ == "__main__":
    sem = BoundedSemaphore(NUM - 1)

    # Create forks
    forks = []
    for n in range(NUM):
        forks.append(Fork(n))

    # Create philosophers
    philosophers = []
    for n in range(1, NUM):
        philosophers.append(Philosopher(n, forks[n], forks[n - 1], sem))
    philosophers.append(Philosopher(0, forks[0], forks[-1], sem))

    # Start each philosopher
    for n in range(NUM):
        philosophers[n].start()


