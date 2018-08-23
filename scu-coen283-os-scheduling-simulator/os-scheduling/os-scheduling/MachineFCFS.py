from Machine import Machine


class MachineFCFS(Machine):
    """
    FCFS scheduling algorithm
    """

    def __init__(self, numCores=1):
        """
        initializes a machine object
        :param numCores: number of cores in the CPU
        """

        Machine.__init__(self, numCores)
