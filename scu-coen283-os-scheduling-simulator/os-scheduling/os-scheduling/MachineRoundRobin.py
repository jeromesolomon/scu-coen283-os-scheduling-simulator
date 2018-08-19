from Machine import Machine


class MachineRoundRobin(Machine):
    """
    Round robin scheduling algorithm

    """
    def __init__(self, numCores=1, quantum=None):
        """
        initializes a machine object
        :param numCores: number of cores in the CPU
        """

        Machine.__init__(self, numCores)

        self.quantum = quantum

    def preempt_cpu(self, process, coreIndex):
        """
        returns false for FCFS scheduling algorithm, since FCFS is not-preemptive
        :param process: the process
        :param coreIndex: the core index
        :return: false
        """

        preempt = False

        if self.time % 3 == 0:
            preempt = True

        return preempt

