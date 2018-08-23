from collections import deque
import Process


class Machine:
    """
    Base machine class implement FCFS scheduling
    """

    def __init__(self, numCores=1):
        """
        initializes a machine object
        :param numCores: number of cores in the CPU
        """

        self.time = 0

        # a process table
        self.processInfoTable = []

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

        # statistics data
        # amount of time the cpu was used
        self.cpuTimeUsed = 0

        # statistics totals and running performance values
        self.statsCPUUtilization = 0
        self.statsThroughput = 0
        self.statsTurnAroundTime = 0
        self.statsWaitTime = 0
        self.statsResponseTime = 0

    def add(self, process):
        """
        Adds a process to the machine
        :param process: the process to add
        :return: None
        """

        # add the process to the new queue
        self.new.append(process)

        # add the process to the process table
        self.processInfoTable.append(process)

    def str_queue(self, qname, q):
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

    def str_process_info_table(self):
        """
        returns a string used to print the process info table
        :return:
        """

        s = ""
        s += "---------------------------------------------"
        s += "\n"

        #
        # construct the header
        #

        s += "Name\tID\tArrival Time"

        # figure out maximum number of burts
        maxNumBursts = 0
        for p in self.processInfoTable:
            maxNumBursts = max(maxNumBursts,len(p.bursts))

        s+= "\t"
        for i in range(0, maxNumBursts):
            s += "Burst " + str(i) + "\t"
        s += "\n"

        #
        # construct the table
        #

        for p in self.processInfoTable:

            s += p.name + "\t"
            s += str(p.id) + "\t"
            s += str(p.startTime) + "\t"

            for b in p.bursts:
                s += "(" + b[0] + "/" + str(b[1]) + ")"
                s += "\t"
            s += "\n"

        s += "---------------------------------------------"
        s += "\n"

        s += ""

        return s

    def __str__(self):
        """
        Returns a string suitable for printing the queue
        :return:
        """
        mystring = "---------------------------------------------" + "\n"
        mystring += "Time : " + str(self.time) + "\n"
        mystring += "Number of cores: " + str(self.numCores) + "\n"

        # the new queues
        mystring += self.str_queue("New queue", self.new)

        # the ready queue
        mystring += self.str_queue("Ready queue", self.ready)
        
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
        mystring += self.str_queue("Blocked queue", self.blocked)

        # the io device
        mystring += "IO:\n"
        if self.io is None:
            mystring += "\t<empty>"
        else:
            mystring += "\t" + str(self.io)
        mystring += "\n"

        # the exit queue
        mystring += self.str_queue("Exit queue", self.exit)

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

    def number_of_processes(self):
        """
        returns the number of processes in the machine
        :return: numProcesses
        """

        numNew = len(self.new)
        numReady = len(self.ready)

        # check all cores for processes
        numCPU = 0
        for core in self.cpu:
            if core is not None:
                numCPU += 1

        numBlocked = len(self.blocked)

        # check io
        if self.io is None:
            numIO = 0
        else:
            numIO = 1

        numExit = len(self.exit)

        total = numNew + numReady + numCPU + numBlocked + numIO + numExit

        return total

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
        
    def __cpu_has_a_core_busy(self):
        """
        Returns true if the cpu has one or more cores busy. if any of the cores has a process then it is busy
        :return:
        """

        # check all the cores to see if any core has a process, if any core has a process return true
        aCoreIsBusy = False
        for core in self.cpu:
            if core is not None:
                aCoreIsBusy = True

        return aCoreIsBusy

    def process_new_queue(self):
        """
        evaluates and advances the new queue
        :return: None
        """

        # if any processes in newQ can proceed put the process in the readyQ

        temp = deque()

        while len(self.new) > 0:

            p = self.new.popleft()

            # if the process p can start put it in the ready q, if not, put it in the tempQ
            if p.startTime <= self.time:
                self.ready.append(p)
            else:
                temp.append(p)

        # put in processes not moved to the ready q back in to the new q
        self.new = temp

    def process_ready_queue(self):
        """
        evaluates and advances the ready queue
        :return: None
        """

        # if any process in readyQ has cpu-burst next, move it to any available core
        # if any process in readyQ has io-burst next, move it to the blocked queue
        while self.__cpu_is_available() and (len(self.ready) > 0):

            # while there's a cpu available and there are processes in the ready queue

            p = self.ready[0]

            if len(p.bursts) == 0:
                print("ERROR: moving process from ready queue directly to exit queue")
                self.exit.append(p)
            else:

                burst = p.bursts[0]

                # if burst is a cpu-burst, move it to the cpu
                if burst[0] == "cpu":
                    self.__add_process_to_cpu(self.ready.popleft())

                # if burst is a io-burst, move it to the blocked queue
                if burst[0] == "io":
                    self.blocked.append(self.ready.popleft())

    def reprocess_ready_queue(self, availableCoreIndex):
        """
        re-processes the ready queue for the cases that a core was made available.  Also, decrements
        the cpu for the process appropriately
        :return: None
        """

        # re-process the ready queue
        self.process_ready_queue()

        # if the core that was made available has a process decrement it's cpu-burst by 1
        # since it will be on the cpu

        if self.cpu[availableCoreIndex] is not None:

            # get the first burst
            burst = self.cpu[availableCoreIndex].bursts[0]

            # if the process is not done with its cpu burst
            if burst[1] > 0:
                # if burst is not done, decrease the cpu-burst value by 1 and leave
                # the process on the cpu for more processing
                self.cpu[availableCoreIndex].bursts[0][1] -= 1
                # increase time on cpu by 1
                self.cpu[availableCoreIndex].timeOnCPUCurrentBurst += 1

    def process_cpu(self):
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
                    # and free up this cpu core.  process ready queue so another process may be able to
                    # take the core which was made available.
                    if len(p.bursts) == 0:
                        p.timeOnCPUCurrentBurst = 0  # reset time on current burst
                        self.exit.append(p)
                        self.cpu[i] = None
                        self.reprocess_ready_queue(i)

                    else:

                        # if next burst is io, move the process to the blocked queue, and process the ready queue
                        # so another process can take the available core
                        if p.bursts[0][0] == "io":
                            p.timeOnCPUCurrentBurst = 0  # reset time on current burst
                            self.blocked.append(p)
                            self.cpu[i] = None
                            self.reprocess_ready_queue(i)

                else:

                    # if burst is not done, decrease the cpu-burst value by 1 and leave
                    # the process on the cpu for more processing
                    p.bursts[0][1] = p.bursts[0][1] - 1

                    # increase time on cpu value
                    p.timeOnCPUCurrentBurst += 1

            i += 1

    def process_blocked_queue(self):
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

    def process_io_stage1(self):
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
                    # if io-burst is done, pop the burst, move
                    # the process to the ready queue or exit queue
                    if burst[1] == 0:
                        # remove the completed io-burst
                        self.io.bursts.popleft()

                        # move the process to the exit queue if there are no more bursts to do
                        if len(self.io.bursts) == 0:
                            self.exit.append(self.io)
                            self.io = None
                    else:
                        # if there are io-burst left to complete, decrement burst by 1
                        self.io.bursts[0][1] -= 1

    def process_io_stage2(self):
        """
        evaluates the io device second stage after the print occurs.  This allows the io to keep the CPU busy my
        moving processes that have completed their IO immediately to the ready queue for cpu
        scheduling on the next loop/cycle of the machine.
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
                    # if io-burst is done, pop the burst, move
                    # the process to the ready queue or exit queue
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
                                # add to ready queue
                                self.ready.append(self.io)
                                # clear the io device
                                self.io = None
                                # in the case that the next burst is io, do nothing.  This will leave the process in io
                                # to complete any remaining io burst
                            
    def process_exit_queue(self):
        """
        handles the exit queue.  processes are simply left in place. But, statistics are gathered.
        :return: returns None
        """
        
        # for each process in exit queue, if this is the first time, set the timestamp.
        for p in self.exit:
            if p.statsFirstTimeInExitQueue:
                p.statsExitQueueTimestamp = self.time
                p.statsFirstTimeInExitQueue = False

    def process_all(self):
        """
        handles the process queues, cpu, and io devices and moving processes around
        :return: returns None
        """

        # adjust processes

        #
        # handle the newQ
        #

        # if any processes in newQ can proceed put them in the readyQ
        self.process_new_queue()

        #
        # handle the readyQ
        #

        # if any process in readyQ has cpu-burst next, move it to any available core
        # if any process in readyQ has io-burst next, move it to the blocked queue
        self.process_ready_queue()

        #
        # handle the CPU
        #

        # if process is done on any of the CPU cores and has io-burst next, move them to blocked queue
        # if process is done on any of the CPU cores and has cpu-burst next, leave it in the CPU
        # if process is done and does not have any more bursts, move it to the exit queue
        self.process_cpu()

        #
        # handle the blockedQ
        #

        # if a process in blocked queue and io is available, move it io
        self.process_blocked_queue()

        #
        # handle the io device
        #

        # if IO is done and process has more burst left, move it to the readyQ
        # if IO is done and does not have any more bursts, move it to the exit queue
        # This is a two stage process.  Stage1 happens before printing data.  Stage2 occurs after printing and the
        # io is complete to move processes immediately to the ready queue
        self.process_io_stage1()
        
        #
        # handles the exit queue
        #
        self.process_exit_queue()

        # check if the machine has processes
        hasProcesses = self.has_processes()

        return hasProcesses
        
    def calculate_statistics(self):
        """
        calculates the statistics
        :return: returns None
        """
        # if the any core has a process, increase the cpu time stats
        if self.__cpu_has_a_core_busy():
            self.cpuTimeUsed += 1

        # for each process if first time in ready queue, set timestamp
        for p in self.ready:
            if p is not None:
                if p.statsFirstTimeInReadyQueue:
                    if p.startTime == 0:
                        p.statsFirstTimeInReadyQueueTimestamp = 0
                    else:
                        p.statsFirstTimeInReadyQueueTimestamp = self.time
                    p.statsFirstTimeInReadyQueue = False

        # for each process if in ready queue, increase total time in ready queue by 1
        for p in self.ready:
            if p is not None:
                p.statsTotalTimeInReadyQueue += 1

        # for each process if first time on CPU, set timestamp
        for p in self.cpu:
            if p is not None:
                if p.statsFirstTimeOnCPU:
                    if p.startTime == 0:
                        p.statsFirstTimeOnCPUTimestamp = 0
                    else:
                        p.statsFirstTimeOnCPUTimestamp = self.time
                    p.statsFirstTimeOnCPU = False

    def print_statistics(self):
        """
        prints the statistics
        :return: returns None
        """
        n = len(self.exit)
        if n == 0:
            return None

        if self.time == 0:
            return None

        print("---------------------------------------------")
        print("Statistics:")
        print("")

        print("CPU utilization %:")
        util = (self.cpuTimeUsed / self.time) * 100
        print("\tCPU utilization = " + str("%.1f" % util) + "%")
        print("")

        print("Throughput:")
        throughput = n / self.time
        print("\tThroughput = " + str("%.4f" % throughput))
        print("")

        # create a sorted exit list
        sortedExit = list()
        for p in self.exit:
            sortedExit.append(p)

        # sort the list based on the process ID
        sortedExit.sort(key=lambda x: x.id)

        print("Turn Around Time:")
        total = 0
        for p in sortedExit:

            s = "\tTurn Around Time of process "
            s += "id #: " + str(p.id)
            s += " name: " + p.name
            s += " = "
            
            # calculate turn around time time
            turnAroundTime = p.statsExitQueueTimestamp - p.statsFirstTimeInReadyQueueTimestamp
            s += str(turnAroundTime)
            
            print(s)
            
            total += turnAroundTime

        average = total / n
        print("\tAverage Turn Around Time = " + ("%.2f" % average))
        print("")

        print("Wait Time:")
        total = 0
        for p in sortedExit:

            s = "\tWait Time of process "
            s += "id #: " + str(p.id)
            s += " name: " + p.name
            s += " = "
            
            # calculate wait time
            waitTime = p.statsTotalTimeInReadyQueue
            s += str(waitTime)
            
            print(s)
            
            total += waitTime

        average = total / n
        print("\tAverage Wait Time = " + ("%.2f" % average))
        print("")

        print("Response Time:")
        total = 0
        for p in sortedExit:

            s = "\tResponse Time of process "
            s += "id #: " + str(p.id)
            s += " name: " + p.name
            s += " = "
            
            # calculate response time
            responseTime = p.statsFirstTimeOnCPUTimestamp - p.startTime
            s += str(responseTime)
            
            print(s)
            
            total += responseTime

        average = total / n
        print("\tAverage Response Time = " + ("%.2f" % average))

        print("---------------------------------------------")

    def csv_process_trace_table_write_header(self, csvFile):
        """
        write a header to the csv file
        :return:
        """

        s = ""

        s += "Time,"

        # new queue
        s += "New Queue,"

        # ready queue
        s += "Ready Queue,"

        # cpu cores
        for i in range(0, len(self.cpu)):
            s += "CPU Core " + str(i) + ","

        # blocked queue
        s += "Blocked Queue,"

        # io device
        s += "IO,"

        # exit queue
        s += "Exit Queue" + "\n"

        csvFile.write(s)

    def csv_process_trace_table_write(self, csvFile):
        """
        write a line to the csv file
        :return:
        """

        s = ""

        numProcesses = self.number_of_processes()

        s += str(self.time) + ","

        # new queue
        for i in range(0, numProcesses):
            qLen = len(self.new)
            if i < qLen:
                s += self.new[i].name + " "
            else:
                s += ""
        s += ","

        # ready queue
        for i in range(0, numProcesses):
            qLen = len(self.ready)
            if i < qLen:
                s += self.ready[i].name + " "
            else:
                s += ""
        s += ","

        # cpu cores
        for i in range(0, len(self.cpu)):
            if self.cpu[i] is None:
                s += ","
            else:
                s += self.cpu[i].name + ","

        # blocked queue
        for i in range(0, numProcesses):
            qLen = len(self.blocked)
            if i < qLen:
                s += self.blocked[i].name + " "
            else:
                s += ""
        s += ","

        # io
        if self.io is None:
            s += ","
        else:
            s += self.io.name + ","

        # exit queue
        for i in range(0, numProcesses - 1):
            qLen = len(self.exit)
            if i < qLen:
                s += self.exit[i].name + " "
            else:
                s += ""
        i = numProcesses - 1
        qLen = len(self.new)
        if i < qLen:
            s += self.exit[i].name + "\n"
        else:
            s += "\n"

        csvFile.write(s)

    def csv_statistics_table_write_header(self, csvFile):
        """
        write a header to the csv file
        :return:
        """

        s = ""

        s += "Time,"

        s += "CPU Utilization,"

        s += "Throughput,"

        s += "Average Turn Around Time,"

        s += "Average Wait Time,"

        s += "Average Response Time Time\n"

        csvFile.write(s)

    def csv_statistics_table_write(self, csvFile):
        """
        write a line to the csv file
        :return:
        """

        if self.time == 0:
            return None

        s = ""

        s += str(self.time) + ","

        # CPU utilization
        util = (self.cpuTimeUsed / self.time) * 100
        s += str("%.1f" % util) + "%" + ","

        # Throughput
        n = self.number_of_processes()
        throughput = n / self.time
        s += str("%.4f" % throughput) + ","

        # create a sorted exit list
        sortedExit = list()
        for p in self.exit:
            sortedExit.append(p)

        # sort the list based on the process ID
        sortedExit.sort(key=lambda x: x.id)

        # Turn Around Time
        total = 0
        for p in sortedExit:
            # calculate turn around time time
            turnAroundTime = p.statsExitQueueTimestamp - p.statsFirstTimeInReadyQueueTimestamp
            total += turnAroundTime

        average = total / n
        s += ("%.2f" % average) + ","

        # Wait Time
        total = 0
        for p in sortedExit:
            # calculate wait time
            waitTime = p.statsTotalTimeInReadyQueue
            total += waitTime

        average = total / n
        s += ("%.2f" % average) + ","

        # Response Time
        total = 0
        for p in sortedExit:
            # calculate response time
            responseTime = p.statsFirstTimeOnCPUTimestamp - p.startTime
            total += responseTime

        average = total / n
        s += ("%.2f" % average) + "\n"

        csvFile.write(s)
