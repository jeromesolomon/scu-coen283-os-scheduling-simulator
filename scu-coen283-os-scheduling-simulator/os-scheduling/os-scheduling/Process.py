import numpy as np
import random
from collections import deque

# this class supports IO only on one channel like the examples given in lecture


class Process:

    # global process id variable (start process IDs at 100)
    globalProcessID = 100

    def __init__(self, name, startTime):
        # this represents the process beginning at the new state

        # assign a unique process ID
        self.id = Process.globalProcessID
        Process.globalProcessID += 1

        self.name = name
        self.startTime = startTime  # the time at which the process enter the system and is put in to the ready queue

        # list of the type of bursts (type,time)
        # for example, [(cpu,4),(io,3),(cpu,2)]

        # list of all bursts in the process
        self.bursts = deque()

        # statistics
        self.turnAroundTime = 0
        self.waitTime = 0
        self.responseTime = 0

    def set_by_stats(self, numBursts, burstMean, burstSD, ioMean, ioSD):
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
            self.add_cpu_burst(int(round(np.random.normal(burstMean, burstSD))))
            if i < numBursts-1:
                self.add_io_burst(int(round(np.random.normal(ioMean, ioSD))))

    def add_cpu_burst(self, cpuBurst):
        """
        Adds a cpu burst to the process
        :param cpuBurst: amoount of time for cpu burst
        :return: None
        """

        b = ["cpu", cpuBurst]

        self.bursts.append(b)

    def add_io_burst(self, ioBurst):
        """
        Adds a IO burst to the process
        :param cpuBurst: amoount of time for cpu burst
        :return: None
        """

        b = ["io", ioBurst]

        self.bursts.append(b)

    def __str__(self):

        result = ""
        result += "process ID: " + str(self.id)
        result += " "
        result += "{"
        result += "name = " + str(self.name) + ", "
        result += "start time = " + str(self.startTime) + ", "
        result += "bursts = " + str(self.bursts)
        result += "}"

        return result
