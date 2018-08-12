import numpy as np
import random
from collections import deque

# this class supports IO only on one channel like the examples given in lecture


class Process:

    # global process id variable (start process IDs at 100)
    globalProcessID = 100

    def __init__(self, processName, delay):
        # this represents the process beginning at the new state

        # assign a unique process ID
        self.processID = Process.globalProcessID
        Process.globalProcessID += 1

        self.processName = processName

        self.delay = delay  # the time at which the process enter the system and is put in to the ready queue
        self.new = True
        self.finished = False
        self.processTimes = deque()  # this is a list of integer times representing the duration of each process burst
        self.io = deque()  # this is a list of all the io operations that happen between processor bursts
        self.blocked = False  # initialized to not blocked
        self.blocker = None  # nothing blocking process yet



    def setbystats(self, numBursts, burstMean, burstSD, ioMean, ioSD):
        """
        Sets the process based on statistics and random values
        :param numBursts:
        :param burstMean:
        :param burstSD:
        :param ioMean:
        :param ioSD
        :return:
        """

        for i in range(numBursts):
            # generate a random time statistically for both process burst time and io time
            self.processTimes.append(int(round(np.random.normal(burstMean, burstSD))))
            if i < numBursts-1:
                io.append(int(round(np.random.normal(ioMean, ioSD))))

    def addcpuburst(self, cpuBurst):
        """
        Adds a cpu burst to the process
        :param cpuBurst: amoount of time for cpu burst
        :return: None
        """

        self.processTimes.append(cpuBurst)

        return None

    def addioburst(self, ioBurst):
        """
        Adds a IO burst to the process
        :param cpuBurst: amoount of time for cpu burst
        :return: None
        """

        self.io.append(ioBurst)

        return None

    def __str__(self):
        result = ""
        result += "process ID: " + str(self.processID) + " name: " + str(self.processName)

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
            self.printqueuechange("New", "Ready")
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
            self.blocker = self.io.popleft()  # our blocker is now the current time
            return True  # notify that process time was zeroed out
        return False

    def decrementIOTime(self, value):
        self.blocker -= value
        if self.blocker <= 0:
            self.blocker = None  # remove blocker
            self.blocked = False  # unblock process
            return True  # notify that IO time was zeroed out
        return False

    def printqueuechange(self,oldQueueName,newQueueName):
        """
        prints a processes queue change info
        :param oldQueueName: name of the old queue
        :param newQueueName: name of the new queue
        :return: None
        """

        print("process queue change:")
        print("\t" + str(self))
        print("\ttime = " + str(self.getTime()))
        print("\tmoved from " + oldQueueName + " queue to " + newQueueName + " queue")
