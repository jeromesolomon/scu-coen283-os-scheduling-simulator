import numpy as np
import IO
import random


class Process:

    def __init__(self, numBursts, burstMean, burstSD, ioOperationList):
        processTimes = list()  # this is a list of integer times representing the duration of each process burst
        io = list()  # this is a list of all the io operations that happen between processor bursts
        blocked = False
        blocker = None
        for i in range(numBursts):
            processTimes.append(int(round(np.random.normal(burstMean, burstSD))))
            io.append(ioOperationList[random.randint(0, len(ioOperationList))])

    def decrement(self, value):
        currentVal = self.processTimes.pop()
        currentVal -= value
        if currentVal == 0:
            self.blocked = True
            self.blocker = io.pop()

    def unblock(self, ioObject):
        if(ioObject == self.blocker):
            self.blocked = False
            self.blocker = None
