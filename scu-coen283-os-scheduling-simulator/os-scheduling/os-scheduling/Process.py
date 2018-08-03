import numpy as np
import random
from collections import deque

# this class supports IO only on one channel like the examples given in lecture


class Process:

    def __init__(self, processID, numBursts, burstMean, burstSD, ioMean, ioSD, delay):
        # this represents the process beginning at the new state

        self.processID = processID

        self.delay = delay
        self.new = True
        self.finished = False
        self.processTimes = deque()  # this is a list of integer times representing the duration of each process burst
        self.io = deque()  # this is a list of all the io operations that happen between processor bursts
        self.blocked = False  # initialized to not blocked
        self.blocker = None  # nothing blocking process yet
        for i in range(numBursts):
            # generate a random time statistically for both process burst time and io time
            self.processTimes.append(int(round(np.random.normal(burstMean, burstSD))))
            if i < numBursts-1:
                io.append(int(round(np.random.normal(ioMean, ioSD))))

    def __str__(self):
        result = ""
        result = result + "process ID: " + str(self.processID) + "\n"
        '''
        result = result + "new: " + str(self.new) + "\n"
        result = result + "finished: " + str(self.finished) + "\n"
        result = result + "process times: " + "\n"
        if len(self.processTimes) > 0:
            for i in self.processTimes:
                result = result + str(i) + " "
            result = result + "\n"
        result = result + "io times" + "\n"
        if len(self.io) > 0:
            for i in self.io:
                result = result + str(i) + " "
            result = result + "\n"
        result = result + "blocked: " + str(self.blocked) + "\n"
        result = result + "blocker: " + str(self.blocker) + "\n"
        '''
        return result

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
        if self.delay <= 0:  # if i don't have to wait any more
            print("went from new to ready!!!!")
            self.new = False  # i'm not new any more
            return True  # notify that delay time was zeroed out
        return False

    def decrementProcessTime(self, value):

        self.processTimes[0] -= value

        if self.processTimes[0] <= 0:
            self.processTimes.popleft()  # remove the process time
            if len(self.processTimes) == 0:  # if no more processes left
                print("setting finished!")
                self.finished = True  # set finished flag
                return True  # notify that process time was zeroed out
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
