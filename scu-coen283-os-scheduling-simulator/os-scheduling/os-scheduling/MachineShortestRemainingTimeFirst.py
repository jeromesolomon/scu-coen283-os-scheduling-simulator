from Machine import Machine


class MachineShortestRemainingTimeFirst(Machine):
    """
    Round robin scheduling algorithm
    """

    def __init__(self, numCores):
        """
        initializes a machine object
        :param numCores: number of cores in the CPU
        """

        Machine.__init__(self, numCores)

    def __preempt_cpu(self, p, coreIndex):
        """
        returns true if the process should be preempted
        :param p: the process
        :param coreIndex: the core index
        :return: true or false
        """

        preempt = False

        # if the process has less time remaining than a process on the ready queue
        cpuBurstTotal = self.__total_remaining_cpu_bursts(p)

        # find out if there is a process on the ready queue with a smaller remaining time
        for pReady in self.ready:
            pReadyBurstTotal = self.__total_remaining_cpu_bursts(pReady)
            if pReadyBurstTotal < cpuBurstTotal:
                preempt = True

        return preempt

    def process_preemption(self):
        """
        move any preempted process to the ready q
        :return:
        """

        # loop through all the cores looking for preempted processes
        for i in range(0, len(self.cpu)):
            p = self.cpu[i]
            if (p is not None) and p.preempt:
                self.ready.append(p)
                self.cpu[i] = None
                p.preempt = False

    def __total_remaining_cpu_bursts(self, p):
        """
        returns the total remaining cpu burst for the process p
        :param p:
        :return:
        """

        # loop through all the remaining bursts in the process calculating the burstTotal
        burstTotal = 0
        if p is not None:
            for b in p.bursts:
                if b[0] == "cpu":
                    burstValue = b[1]
                    burstTotal += burstValue

        return burstTotal

    def __shortest_remaining_time_in_ready_queue(self):
        """
        returns the index of the process in the ready queue with the shortest cpu burst
        :return: index of process
        """
        # set minimum values to none
        minBurstTotal = None
        minProcessIndex = None

        # loop through the ready queue to find the smallest total remaining cpu bursts
        for i in range(0, len(self.ready)):
            p = self.ready[i]

            if p is not None:
                # loop through all the remaining bursts in the process calculating the burstTotal
                burstTotal = self.__total_remaining_cpu_bursts(p)

                # set value to burst value if min has not been established
                if minBurstTotal is None:
                    minBurstTotal = burstTotal
                    minProcessIndex = i

                # find the shortest burst value
                if burstTotal < minBurstTotal:
                    minBurstTotal = burstTotal
                    minProcessIndex = i

        return minProcessIndex

    def process_ready_queue(self):
        """
        evaluates and advances the ready queue
        :return: None
        """

        # if any process in readyQ has cpu-burst next, move the shortest cpu-burst to any available core
        # if any process in readyQ has io-burst next, move the shortest cpu-burst to the blocked queue

        while self.cpu_is_available() and (len(self.ready) > 0):

            # while there's a cpu available and there are processes in the ready queue

            shortestIndex = self.__shortest_remaining_time_in_ready_queue()
            p = self.ready[shortestIndex]

            if len(p.bursts) == 0:
                print("ERROR: moving process from ready queue directly to exit queue")
                self.exit.append(p)
            else:

                burst = p.bursts[0]

                # if burst is a cpu-burst, move it to the cpu
                if burst[0] == "cpu":
                    self.add_process_to_cpu(p)
                    self.ready.remove(p)

                # if burst is a io-burst, move it to the blocked queue
                if burst[0] == "io":
                    self.blocked.append(p)
                    self.ready.remove(p)

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

                    # check if process should be preempted
                    # if preempted and the ready queue has other processes to put on the CPU, then
                    # put the current process on to the ready queue
                    if self.__preempt_cpu(p, i) and (len(self.ready) > 0):
                        p.timeOnCPUCurrentBurst = 0
                        p.preempt = True

            i += 1

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

        # handle preemption
        self.process_preemption()

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
                mystring += " timeOnCPUCurrentBurst = " + str(p.timeOnCPUCurrentBurst)
                mystring += " ,quantum = " + str(p.quantum)
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