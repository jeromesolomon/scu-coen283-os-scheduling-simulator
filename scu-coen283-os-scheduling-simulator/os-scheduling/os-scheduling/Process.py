import numpy as np
import random
from collections import deque

# this class supports IO only on one channel like the examples given in lecture


class Process:

    def __init__(self, numBursts, burstMean, burstSD, ioMean, ioSD):
        # this represents the process beginning at the new state
        self.processTimes = deque()  # this is a list of integer times representing the duration of each process burst
        self.io = deque()  # this is a list of all the io operations that happen between processor bursts
        self.blocked = False  # initialized to not blocked
        self.blocker = None  # nothing blocking process yet
        for i in range(numBursts):
            # generate a random time statistically for both process burst time and io time
            processTimes.append(int(round(np.random.normal(burstMean, burstSD))))
            io.append(int(round(np.random.normal(ioMean, ioSD))))

    def getTime(self):
        # returns time to next action regardless of whether blocked or processing.
        if self.blocked:
            return self.blocker
        return self.processTimes[0]

    def decrement(self, value):
        if self.blocked:
            self.decrementIOTime(value)
        else:
            self.decrementProcessTime(value)

    def decrementProcessTime(self, value):

        processTimes[0] -= value

        if processTimes[0] == 0:
            processTimes.popleft()  # remove the process time
            self.blocked = True  # block process
            self.blocker = io.popleft()  # our blocker is now the current time

    def decrementIOTime(self, value):
        self.blocker -= value
        if self.blocker == 0:
            self.blocker = None  # remove blocker
            self.blocked = False  # unblock process
