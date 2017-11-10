from threading import Thread
from time import sleep

from queue import Queue


class Node:
    def __init__(self, target, inputs, num_outputs):
        self.target = target

        self.inputs = inputs

        self.out = []
        for _ in range(num_outputs):
            self.out.append(Queue())

    def run(self):
        while True:
            args = self.inputs + self.out
            self.target(*args)


class PeriodicNode(Node):
    # noinspection PyMissingConstructor
    def __init__(self, period):
        self.period = period
        self.out = [Queue()]

    def run(self):
        while True:
            self.out[0].put(None)
            sleep(self.period)


class RateLimitedNode(Node):
    def __init__(self, target, interval, inputs, num_outputs=1):
        super(RateLimitedNode, self).__init__(target=target, inputs=inputs, num_outputs=num_outputs)
        self.interval = interval

    def run(self):
        while True:
            t = Thread(target=sleep, args=(self.interval,))
            t.start()
            args = self.inputs + self.out
            self.target(*args)
            t.join()
