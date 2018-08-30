from PreemptiveMachine import PreemptiveMachine
from FPPQ import FPPQ


class FPPQMachine(PreemptiveMachine):

    def __init__(self, numCores):
        """
        initializes a machine object
        :param numCores: number of cores in the CPU
        """
        PreemptiveMachine.__init__(self, FPPQ(), numCores)

    def __preempt_cpu(self, p, coreIndex):
        """
        returns true if the process should be preempted
        :param p: the process
        :param coreIndex: the core index
        :return: true or false
        """

        if p.timeOnCPUCurrentBurst > p.quantum or self.ready.preempt(p):
            # set the process preemption fields
            p.preempt = True

        return p.preempt
