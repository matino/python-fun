from threading import Thread, BoundedSemaphore, Lock
from random import randint
from time import sleep

NUM = 3


class Fork(object):
    def __init__(self, fork_id):
        self.lock = Lock()
        self._id = fork_id

    def grab(self, person_id):
        self.lock.acquire()
        print "Fork# %d was grabbed by philosopher# %d" % (self._id, person_id)

    def lay_down(self, person_id):
        print "Fork# %d was layed down by philosopher# %d" % (self._id, person_id)
        self.lock.release()

    def __str__(self):
        return "Fork# %d" % self._id


class Philosopher(Thread):
    def __init__(self, id_, left_fork, right_fork, sem, *args, **kwargs):
        super(Philosopher, self).__init__(*args, **kwargs)
        self._id = id_
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.semaphore = sem

    def run(self):
        while True:
            self._think()
            self._eat()

    def _think(self):
        print "Philosopher# %d is thinking" % self._id
        sleep(randint(3, 5))

    def _eat(self):
        print "Philosopher# %d is hungry" % self._id

        with self.semaphore:
            self.left_fork.grab(self._id)
            sleep(3)
            self.right_fork.grab(self._id)

            print "Philosopher# %d is eating" % self._id

            sleep(randint(1, 3))
            self.left_fork.lay_down(self._id)
            self.right_fork.lay_down(self._id)

            print "Philosopher# %d finished eating" % self._id


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
