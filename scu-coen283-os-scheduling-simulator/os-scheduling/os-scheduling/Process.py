import numpy as np
import random
from collections import deque

# this class supports IO only on one channel like the examples given in lecture


class Process:

    # global process id variable (start process IDs at 100)
    globalProcessID = 100

    def __init__(self, name, startTime, quantum, priority=0):
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

        # allotted time quantum:
        self.quantum = 0

        # was the process preempted?:
        self.preempted = False

        # process priority (used for priority queue, multilevel [feedback] queue)
        # priority always starts high unless otherwise noted.
        self.priority = priority

        # support for scheduling algorithms
        # time on CPU for the current burst.  Used for round robin scheduling algorithm
        self.timeOnCPUCurrentBurst = 0

        #support for CFS
        self.vruntime = None
        self.cputime = 0

        # statistics

        self.statsFirstTimeInReadyQueue = True
        
        # turn around time stats & response time stats
        self.statsFirstTimeInReadyQueueTimestamp = 0

        self.statsFirstTimeInExitQueue = True
        self.statsExitQueueTimestamp = 0
        
        # wait time
        self.statsTotalTimeInReadyQueue = 0

        # response time
        self.statsFirstTimeOnCPU = True
        self.statsFirstTimeOnCPUTimestamp = 0

        # preempt boolean
        self.preempt = False
        # process that preempted
        self.preemptedByReadyQueueIndex = None

        # time quantum per process for scheduling algorithms that need it MFQ, RR, et cetera
        self.quantum = quantum

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
            self.add_cpu_burst(max(1, int(round(np.random.normal(burstMean, burstSD)))))
            if i < numBursts-1:
                self.add_io_burst(max(1, int(round(np.random.normal(ioMean, ioSD)))))

    def add_cpu_burst(self, cpuBurst):
        """
        Adds a cpu burst to the process
        :param cpuBurst: amoount of time for cpu burst
        :return: None
        """
        if cpuBurst > 0:
            b = ["cpu", cpuBurst]
            self.bursts.append(b)

    def add_io_burst(self, ioBurst):
        """
        Adds a IO burst to the process
        :param ioBurst: amount of time for cpu burst
        :return: None
        """
        if ioBurst > 0:
            b = ["io", ioBurst]
            self.bursts.append(b)

    def __str__(self):

        result = ""
        result += "process ID: " + str(self.id)
        result += " "
        result += "{"
        result += "name = " + str(self.name) + ", "
        result += "quantum =" + str(self.quantum) + ", "
        result += "start time = " + str(self.startTime) + ", "
        result += "bursts = " + str(self.bursts)
        result += "}"

        return result
