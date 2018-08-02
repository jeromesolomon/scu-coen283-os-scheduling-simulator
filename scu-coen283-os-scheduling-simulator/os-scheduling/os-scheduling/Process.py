import numpy as np
import random
from collections import deque

# this class supports IO only on one channel like the examples given in lecture


class Process:

    def __init__(self, numBursts, burstMean, burstSD, ioMean, ioSD, delay):
        # this represents the process beginning at the new state

        self.delay = delay
        self.new = True
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
        if self.new:
            return self.delay
        if self.blocked:
            return self.blocker
        return self.processTimes[0]

    def decrement(self, value):
        if self.new:
            return self.decrementDelayTime(value)
        elif self.blocked:
            return self.decrementIOTime(value)
        else:
            return self.decrementProcessTime(value)

    def decrementDelayTime(self, value):
        self.delay -= value  # remove process time
        if delay <= 0:  # if i don't have to wait any more
            new = False  # i'm not new any more
            return True  # notify that delay time was zeroed out
        return False

    def decrementProcessTime(self, value):

        processTimes[0] -= value

        if processTimes[0] <= 0:
            processTimes.popleft()  # remove the process time
            self.blocked = True  # block process
            self.blocker = io.popleft()  # our blocker is now the current time
            return True  # notify that process time was zeroed out
        return False

    def decrementIOTime(self, value):
        self.blocker -= value
        if self.blocker <= 0:
            self.blocker = None  # remove blocker
            self.blocked = False  # unblock process
            return True  # notify that IO time was zeroed out
        return False
