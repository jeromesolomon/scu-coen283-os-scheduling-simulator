from collections import deque
import Process

class Machine:

    def __init__(self, numCores = 1):
        """
        Initializes a machine object
        :param numCores: number of cores in the CPU
        """

        self.time = 0

        # cpu is a list of processes of size numCores (each representing a core on the cpu)
        self.numCores = numCores
        self.cpu = [None] * numCores

        # io is a single device that handles only 1 io burst at a time
        self.io = None

        # queue for os handling of processes
        self.new = deque()
        self.ready = deque()
        self.blocked = deque()
        self.exit = deque()

    def add(self, process):
        """
        Adds a process to the machine
        :param process: the process to add
        :return: None
        """
        self.new.append(process)

    def __str_queue(self,qname,q):
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
        mystring += "Time : " + str(self.time) + "\n"
        mystring += "Number of cores: " + str(self.numCores) + "\n"

        # the new queues
        mystring += self.__str_queue("New queue", self.new)

        # the ready queue
        mystring += self.__str_queue("Ready queue", self.ready)
        
        # the running/CPU processes
        mystring += "CPU:\n"
        coreNum = 0
        for p in self.cpu:
            mystring += "\tcore " + str(coreNum) + ": "
            if p is None:
                mystring += "<empty>"
            else:
                mystring += str(p)
            mystring += "\n"
            coreNum += 1

        # the blocked queue
        mystring += self.__str_queue("Blocked queue", self.blocked)

        # the io device
        mystring += "IO:\n"
        if self.io is None:
            mystring += "\t<empty>"
        else:
            mystring += "\t" + str(self.io)
        mystring += "\n"

        # the exit queue
        mystring += self.__str_queue("Exit queue", self.exit)

        mystring += "---------------------------------------------" + "\n"

        return mystring

    def has_processes(self):
        """
        Does the machine have processes in it
        :return: True if the machine has processes
        """

        cpu = False
        for core in self.cpu:
            if core is not None:
                cpu = True

        newQ = len(self.new)
        readyQ = len(self.ready)
        blockedQ = len(self.blocked)

        status = cpu or newQ or readyQ or blockedQ

        return status

    def __advance_new_queue(self):
        """
        evaluates and advances the new queue
        :return: None
        """

        print("status: advancing the new queue")

    def advance_time(self):
        """
        Adjust processes then moves the clock 1 tick forward (time + 1)
        :return: returns done as True if all processes are completed
        """

        hasProcesses = False

        # adjust processes

        #
        # handle the newQ
        #

        # if any processes in newQ can proceed put them in the readyQ

        #
        # handle the readyQ
        #

        # if any process in readyQ has cpu-burst next, move it to any available core

        # if any process in readyQ has io-burst next, move it to the blocked queue

        #
        # handle the CPU
        #

        # if process is done on any of the CPU cores and has io-burst next, move them to blocked queue

        # if process is done on any of the CPU cores and has cpu-burst next, leave it in the CPU

        # if process is done and does not have any more bursts, move it to the exit queue

        #
        # handle the blockedQ
        #

        # if a process in blocked queue and io is available, move it io

        #
        # handle the blockedQ
        #

        # if IO is done and process has more burst left, move it to the readyQ

        # if IO is done and does not have any more bursts, move it to the exit queue


        """
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
        # print("times = " + str(times))
        delta = min(times)
        self.machineTime += delta

        if len(self.blocked) > 0 and self.blocked[0].decrement(delta):
            # if there is something self.blocked and this time advancement zeroes out the wait time of the frontmost process
            
            # dequeue from self.blocked and enqueue into self.ready
            p = self.blocked.popleft()
            self.ready.append(p)
            p.print_queue_change("Blocked", "Ready")

        if self.running != None:
            if self.running.decrement(delta):
                # if there is something running and this time advancement zeroes out its burst time
                if self.running.finished:
                    # add to the finished queue
                    p = self.running
                    self.exit.append(p)
                    p.print_queue_change("CPU","Exit")
                    
                else:
                		# it's self.blocked now (internal flagging happened already)
                    p = self.running
                    self.blocked.append(p)
                    p.print_queue_change("CPU","Blocked")
                self.running = None  # set running to None
            elif preempt:  # when preemption happens, it always removes the process from running and puts it into self.ready
            		# put it back into the self.ready queue
                p = self.running
                self.ready.append(p)
                p.print_queue_change("CPU","Ready")
                self.running = None  # set running to None

        if len(self.ready) > 0 and self.running == None:  # if there's something self.ready and nothing running
            # take the frontmost element out of the self.ready queue and put it into the running spot
            p = self.ready.popleft()
            self.running = p
            p.print_queue_change("Ready", "CPU")

        if len(self.new) > 0 and self.new[0].decrement(delta):
            # if there is a self.new process and this time advancement zeroes out the delay of the frontmost process
            # take process from self.new and put it into self.ready
            p = self.new.popleft()
            self.ready.append(p)
            p.print_queue_change("New", "Ready")

        """

        # check if the machine has processes
        haaProcesses = self.has_processes()

        # if cpu has processes in new, ready, blocked, or cpu, increase time by 1
        if hasProcesses:
            self.time += 1

        return hasProcesses

    def print_queue_change(self, p, oldQueueName, newQueueName):
        """
        prints a processes queue change info
        :param p: the process changing queues
        :param oldQueueName: name of the old queue
        :param newQueueName: name of the new queue
        :return: None
        """

        print("process queue change:")
        print("\ttime = " + str(self.time))
        print("\t" + str(p))
        print("\tmoved from " + oldQueueName + " queue to " + newQueueName + " queue")