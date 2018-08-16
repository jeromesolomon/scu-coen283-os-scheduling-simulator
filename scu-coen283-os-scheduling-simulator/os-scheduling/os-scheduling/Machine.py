from collections import deque
import Process


class Machine:

    def __init__(self):
        self.machineTime = 0
        self.new = deque()
        self.ready = deque()  # This is where the DataStructures class will apply.
        self.running = None
        self.blocked = deque()
        self.exit = deque()
        self.quantum = Quantum(500)
        self.useQuantum = False

    def add(self, process):
        self.new.append(process)

    def __strqueue(self, qname, q):
        """
        Private method used to print a queue neatly.
        :param qname: name of the queue
        :param q: the queue
        :return: a string
        """

        mystring = ""
        mystring += qname + ":" + "\n"
        if len(q) == 0:
            mystring += "\t" + "<empty>" + "\n"
        else:
            for p in q:
                mystring += "\t" + str(p) + "\n"

        return mystring

    def __str__(self):
        """
        Returns a string suitable for printing the queue
        :return:
        """
        mystring = "---------------------------------------------" + "\n"
        mystring += "Time : " + str(self.machineTime) + "\n"

        # the new queues
        mystring += self.__strqueue("New queue", self.new)

        # the ready queue
        mystring += self.__strqueue("Ready queue", self.ready)

        # the running/CPU process
        mystring += "CPU :\n"
        mystring += "\t"
        if self.running == None:
            mystring += "<empty>"
        else:
            mystring += str(self.running)
        mystring += "\n"

        # the blocked queue
        mystring += self.__strqueue("Blocked queue", self.blocked)

        # the exit queue
        mystring += self.__strqueue("Exit queue", self.exit)

        mystring += "---------------------------------------------" + "\n"

        return mystring

    def advanceTime(self):
        # returns False if time was not advanced, True if it was
        # self.newTime is the time until arrival

        newTime = self.new[0].getTime() if len(self.new) > 0 else None
        runningTime = None if self.running is None else self.running.getTime()
        blockedTime = None if len(self.blocked) == 0 else self.blocked[0].getTime()
        quantumTime = None if self.useQuantum is False else self.quantum.getTime()
        times = list()

        if newTime is not None:
            times.append(newTime)
        if runningTime is not None:
            times.append(runningTime)
        if blockedTime is not None:
            times.append(blockedTime)
        if quantumTime is not None:
            times.append(quantumTime)

        if len(times) == 0:
            return False  # this means that the new queue is empty, the running state is empty, and the self.blocked queue is empty
        # print("times = " + str(times))
        delta = min(times)
        self.machineTime += delta
        preempt = self.quantum.decrement(delta) #decrement and set preemption here

        if len(self.blocked) > 0 and self.blocked[0].decrement(delta):
            # if there is something self.blocked and this time advancement zeroes out the wait time of the frontmost process

            # dequeue from self.blocked and enqueue into self.ready
            p = self.blocked.popleft()
            self.ready.append(p)
            p.printqueuechange("Blocked", "Ready")

        if self.running is not None:
            if self.running.decrement(delta):
                # if there is something running and this time advancement zeroes out its burst time
                if self.running.finished:
                    # add to the finished queue
                    p = self.running
                    self.exit.append(p)
                    p.printqueuechange("CPU", "Exit")

                else:
                    # it's self.blocked now (internal flagging happened already)
                    p = self.running
                    self.blocked.append(p)
                    p.printqueuechange("CPU", "Blocked")
                self.running = None  # set running to None
            elif preempt:  # when preemption happens, it always removes the process from running and puts it into self.ready
                # put it back into the self.ready queue
                p = self.running
                self.ready.append(p)
                p.printqueuechange("CPU", "Ready")
                self.running = None  # set running to None

        if len(self.ready) > 0 and self.running is None:  # if there's something self.ready and nothing running
            # take the frontmost element out of the self.ready queue and put it into the running spot
            p = self.ready.popleft()
            self.running = p
            p.printqueuechange("Ready", "CPU")

        if len(self.new) > 0 and self.new[0].decrement(delta):
            # if there is a self.new process and this time advancement zeroes out the delay of the frontmost process
            # take process from self.new and put it into self.ready
            p = self.new.popleft()
            self.ready.append(p)
            p.printqueuechange("New", "Ready")

        return True  # do this at the end because two of the above blocks may execute during the same time slice


class Quantum:

    def __init__(self, qTime):
        self.qTime = qTime
        self.timeRemaining = qTime

    def setQuantum(self, qTime):
        self.qTime = qTime

    def getTime(self):
        return self.timeRemaining

    def decrement(self, time):
        self.timeRemaining -= time
        expired = self.timeRemaining <= 0
        # if time quantum is expired, reset time
        if expired:
            self.timeRemaining = self.qTime
        return expired

