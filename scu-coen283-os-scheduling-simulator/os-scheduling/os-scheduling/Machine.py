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

    def add(self, process):
        self.new.append(process)

    def __strqueue(self,qname,q):
        """
        Private method used to print a queue neatly.
        :param qname: name of the queue
        :param q: the queue
        :return: a string
        """

        mystring = ""
        mystring += qname + ":" + "\n"
        if len(self.new) == 0:
            mystring += "\t" + "<empty>" + "\n"
        else:
            for p in self.new:
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

        # the running/CPU queue
        mystring += self.__strqueue("CPU (running)", self.running)

        # the blocked queue
        mystring += self.__strqueue("Blocked queue", self.blocked)

        # the exit queue
        mystring += self.__strqueue("Exit queue", self.exit)

        mystring += "---------------------------------------------" + "\n"

        return mystring

    def advanceTime(self):
        # returns False if time was not advanced, True if it was
        # self.newTime is the time until arrival

        preempt = False  # this should get set if a preemption happens
        newTime = self.new[0].getTime() if len(self.new) > 0 else None
        runningTime = None if self.running == None else self.running.getTime()
        blockedTime = None if len(self.blocked) == 0 else self.blocked[0].getTime()
        times = list()

        if(newTime != None):
            times.append(newTime)
        if(runningTime != None):
            times.append(runningTime)
        if(blockedTime != None):
            times.append(blockedTime)

        if(len(times) == 0):
            return False  # this means that the new queue is empty, the running state is empty, and the self.blocked queue is empty
        print("times = ")
        print(times)
        delta = min(times)
        self.machineTime += delta

        if len(self.blocked) > 0 and self.blocked[0].decrement(delta):
            # if there is something self.blocked and this time advancement zeroes out the wait time of the frontmost process
            self.ready.append(self.blocked.popleft())  # dequeue from self.blocked and enqueue into self.ready

        if self.running != None:
            if self.running.decrement(delta):
                # if there is something running and this time advancement zeroes out its burst time
                if self.running.finished:
                    self.exit.append(self.running)  # add to the finished queue
                else:
                    self.blocked.append(self.running)  # it's self.blocked now (internal flagging happened already)
                self.running = None  # set running to None
            elif preempt:  # when preemption happens, it always removes the process from running and puts it into self.ready
                self.ready.append(self.running)  # put it back into the self.ready queue
                self.running = None  # set running to None

        if len(self.ready) > 0 and self.running == None:  # if there's something self.ready and nothing running
            print("first item in self.ready")
            print(self.ready[0])
            self.running = self.ready.popleft()  # take the frontmost element out of the self.ready queue and put it into the running spot
            print("self.ready's size")
            print(len(self.ready))
            print("self.running")
            print(self.running)

        if len(self.new) > 0 and self.new[0].decrement(delta):
            # if there is a self.new process and this time advancement zeroes out the delay of the frontmost process
            self.ready.append(self.new.popleft())  # take process from self.new and put it into self.ready

        return True  # do this at the end because two of the above blocks may execute during the same time slice
