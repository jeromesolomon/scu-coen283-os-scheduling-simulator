from Machine import Machine


class MachineRoundRobin(Machine):
    """
    Round robin scheduling algorithm

    """
    def __init__(self, numCores, quantum):
        """
        initializes a machine object
        :param numCores: number of cores in the CPU
        """

        Machine.__init__(self, numCores)

        self.quantum = quantum

    def __preempt_cpu(self, p, coreIndex):
        """
        returns true if the process should be preempted
        :param p: the process
        :param coreIndex: the core index
        :return: true or false
        """

        preempt = False

        if p.timeOnCPUCurrentBurst >= self.quantum:
            preempt = True

        return preempt

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
                        self.ready.append(p)
                        self.cpu[i] = None
                        self.reprocess_ready_queue(i)

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
