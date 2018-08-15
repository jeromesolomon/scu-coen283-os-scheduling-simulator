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

        newQ = (len(self.new) > 0)
        readyQ = (len(self.ready) > 0)
        blockedQ = (len(self.blocked) > 0)

        status = cpu or newQ or readyQ or blockedQ

        return status

    def __add_process_to_cpu(self, p):
        """
        Adds a process to an available slot on the cpu
        :param p:
        :return: None
        """

        assigned = False
        i = 0

        # loop through the cores adding a process to any available core
        while (i < len(self.cpu)) and (not assigned):

            if self.cpu[i] is None:
                self.cpu[i] = p
                assigned = True

            i += 1

    def __cpu_is_available(self):
        """
        Returns true if the cpu is empty
        :return:
        """

        # check all the cores to see if any core is available, if any core is available
        # return true
        isAvailable = False
        for core in self.cpu:
            if core is None:
                isAvailable = True

        return isAvailable

    def __process_new_queue(self):
        """
        evaluates and advances the new queue
        :return: None
        """

        # if any processes in newQ can proceed put them in the readyQ

        temp = deque()

        while len(self.new) > 0:

            p = self.new.pop()

            # if the process p can start put it in the ready q, if not, put it in the tempQ
            if p.startTime <= self.time:
                self.ready.append(p)
            else:
                temp.append(p)

        # put in processes not moved to the ready q back in to the new q
        self.new = temp

    def __process_ready_queue(self):
        """
        evaluates and advances the ready queue
        :return: None
        """

        temp = deque()

        # if any process in readyQ has cpu-burst next, move it to any available core
        # if any process in readyQ has io-burst next, move it to the blocked queue

        while len(self.ready) > 0:

            p = self.ready.pop()

            # if any process in readyQ has cpu-burst next, move it to any available core
            # if remaining bursts are 0, the process is done and should be in the exit queue

            if len(p.remainingBursts) == 0:
                print("ERROR: moving process from ready queue directly to exit queue")
                self.exit.append(p)
            else:
                burst = p.remainingBursts[0]
                if burst[0] == "cpu":

                    # if cpu is available add process to cpu, otherwise leave it in the ready q
                    if self.__cpu_is_available():
                        self.__add_process_to_cpu(p)
                    else:
                        temp.append(p)

                if burst[0] == "io":
                    self.blocked.append(p)

        # put in processes not moved to the cpu or blocked q back in to the ready q
        self.ready = temp



    def process_all_queues(self):
        """
        handles the process queues and moving processes around
        :return: returns None
        """

        hasProcesses = False

        # adjust processes

        #
        # handle the newQ
        #

        # if any processes in newQ can proceed put them in the readyQ
        self.__process_new_queue()

        #
        # handle the readyQ
        #

        # if any process in readyQ has cpu-burst next, move it to any available core
        # if any process in readyQ has io-burst next, move it to the blocked queue
        self.__process_ready_queue()

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



        # check if the machine has processes
        hasProcesses = self.has_processes()

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