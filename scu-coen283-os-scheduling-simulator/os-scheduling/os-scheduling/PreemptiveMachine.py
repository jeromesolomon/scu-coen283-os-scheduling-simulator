from Machine2 import Machine2
import RR


class PreemptiveMachine(Machine2):
    """
    Round robin scheduling algorithm

    """
    def __init__(self, structure, numCores):
        """
        initializes a machine object
        :param numCores: number of cores in the CPU
        """
        Machine2.__init__(self, structure, numCores)

    def __preempt_cpu(self, p, coreIndex):
        """
        returns true if the process should be preempted
        :param p: the process
        :param coreIndex: the core index
        :return: true or false
        """

        if p.timeOnCPUCurrentBurst > p.quantum:
            # set the process preemption fields
            p.preempt = True

        return p.preempt

    def __process_preemption(self):
        """
        move any preempted process to the ready q
        :return:
        """

        # loop through all the cores looking for preempted processes
        for i in range(0, len(self.cpu)):
            p = self.cpu[i]
            if (p is not None) and p.preempt:
<<<<<<< HEAD:scu-coen283-os-scheduling-simulator/os-scheduling/os-scheduling/MachineRoundRobin.py

                # remove the preemptedBy process
                preemptedBy = self.ready.popleft()

                # reset preemption values, and put the preempted process on the ready queue
                # adding back its cpu time so that it doesnt appear to have been on the cpu
                p.preempt = False
                p.bursts[0][1] += 1
                p.timeOnCPUCurrentBurst = 0
                self.ready.append(p)

                # take the preemptedBy process, and put it on the cpu as if it has been on
                # the cpu for 1 cycle
                if preemptedBy.bursts[0][1] > 0:
                    preemptedBy.bursts[0][1] = preemptedBy.bursts[0][1] - 1

                # increase time on cpu value
                preemptedBy.timeOnCPUCurrentBurst += 1

                # add it on to the cpu
                self.cpu[i] = preemptedBy
=======
                self.ready.add(p)
                self.cpu[i] = None
                # p.preempt = False  # i want to retain the flag so that MFQ can know when something was preempted
>>>>>>> MFQ:scu-coen283-os-scheduling-simulator/os-scheduling/os-scheduling/PreemptiveMachine.py

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

                    #increase cputime for process
                    p.cputime += 1

                    # check if process should be preempted
                    # if preempted and the ready queue has other processes to put on the CPU, then
                    # put the current process on to the ready queue
                    if self.__preempt_cpu(p, i) and self.ready.size > 0:
                        p.timeOnCPUCurrentBurst = 0
                        self.__process_preemption()

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
        mystring += self.str_queue("Ready queue", self.ready.toQueue())

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