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

    def __str_queue(self, qname, q):
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

        newQ = (len(self.new) > 0)
        readyQ = (len(self.ready) > 0)

        # check all cores for processes
        cpu = False
        for core in self.cpu:
            if core is not None:
                cpu = True


        blockedQ = (len(self.blocked) > 0)

        # check io
        io = (self.io is not None)

        status = newQ or readyQ or cpu or blockedQ or io

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
                temp.appendleft(p)

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

            if len(p.bursts) == 0:
                print("ERROR: moving process from ready queue directly to exit queue")
                self.exit.append(p)
            else:
                burst = p.bursts[0]
                if burst[0] == "cpu":

                    # if cpu is available add process to cpu, otherwise leave it in the ready q
                    if self.__cpu_is_available():
                        self.__add_process_to_cpu(p)
                    else:
                        temp.appendleft(p)
                # if burst is an io-burst, move it to the blocked queue
                if burst[0] == "io":
                    self.blocked.append(p)

        # put that processes that were not moved to the cpu or blocked q back in to the ready q
        self.ready = temp


    def __process_cpu(self):
        """
        evaluates and handles processes in the cpu, moving them to appropriate queues
        when they are done
        :return: None
        """


        # for each process on the CPU, check if the cpu burst is done and
        # process it.
        # if process is done on any of the CPU cores and has io-burst next, move it to blocked queue
        # if process is done on any of the CPU cores and has cpu-burst next, leave it in the CPU
        # if process is done and does not have any more bursts, move it to the exit queue

        i = 0
        while i < len(self.cpu):
            p = self.cpu[i]

            # if this core has a process
            if p is not None:

                # get the first burst
                burst = p.bursts[0]

                # the cpu-burst is done when there is no more time left in the burst value
                burstIsDone = (burst[1] == 0)
                if burstIsDone:
                    # pop the burst off the bursts queue
                    p.bursts.popleft()

                    # if there are no more burst left, we are done.  Move process to the exit queue
                    # and free up this cpu core.
                    if len(p.bursts) == 0:
                        self.exit.append(p)
                        self.cpu[i] = None
                    else:
                        # if next burst is io, move the process to the blocked queue
                        if p.bursts[0][0] == "io":
                            self.blocked.append(p)
                            self.cpu[i] = None

                else:
                    # if burst is not done, decrease the cpu-burst value by 1 and leave
                    # the process on the cpu for more processing
                    p.bursts[0][1] = p.bursts[0][1] - 1

            i += 1

    def __process_blocked_queue(self):
        """
        evaluates and advances the blocked queue
        :return: None
        """

        # if a process is in blocked queue and io is available, move it io

        if (len(self.blocked) > 0) and (self.io is None):

            # remove the process from the blocked queue
            p = self.blocked.pop()

            # put the process in to io
            self.io = p

    def __process_io(self):
        """
        evaluates the io device
        :return: None
        """

        # if there is a process in io
        if self.io is not None:
            # if the process has no bursts left, send it to exit queue
            if len(self.io.bursts) == 0:
                self.exit.append(self.io)
                self.io = None
            else:
                burst = self.io.bursts[0]
                # if the next burst is for cpu, move it to the ready queue
                if burst[0] == "cpu":
                    self.ready.append(self.io)
                    self.io = None
                if burst[0] == "io":
                    # if io-burst is done, pop the burst, move the process to the ready queue or exit queue
                    if burst[1] == 0:
                        # remove the completed io-burst
                        self.io.bursts.popleft()

                        # move the process to the exit queue if there are no more bursts to do
                        if len(self.io.bursts) == 0:
                            self.exit.append(self.io)
                            self.io = None
                        else:
                            nextBurst = self.io.bursts[0]
                            # move the process to the ready queue if there are more cpu bursts to do
                            if nextBurst[0] == "cpu":
                                self.ready.append(self.io)
                                self.io = None
                            # in the case that the next burst is io, do nothing.  This will leave the process in io
                            # to complete any remaining io bursts
                    else:
                        # if there are io-burst left to complete, decrement burst by 1
                        self.io.bursts[0][1] -= 1

    def process_all(self):
        """
        handles the process queues, cpu, and io devices and moving processes around
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
        self.__process_cpu()

        #
        # handle the blockedQ
        #

        # if a process in blocked queue and io is available, move it io
        self.__process_blocked_queue()

        #
        # handle the io device
        #

        # if IO is done and process has more burst left, move it to the readyQ
        # if IO is done and does not have any more bursts, move it to the exit queue
        self.__process_io()

        # check if the machine has processes
        hasProcesses = self.has_processes()

        return hasProcesses
