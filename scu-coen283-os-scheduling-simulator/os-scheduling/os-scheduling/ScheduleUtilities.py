import Machine
import Process

"""
Utility functions for schedule toolset
"""


def create_lecture_example():
    """
    Creates the example of four processes from Professor Amr Elkady's lecture
    :return: returns a machine with the lecture example processes
    """

    #
    # Professor Amr Elkady's class lecture example
    #

    machine = Machine.Machine()

    # process A
    processA = Process.Process("A", 0)

    processA.add_cpu_burst(4)
    processA.add_io_burst(4)
    processA.add_cpu_burst(4)
    processA.add_io_burst(4)
    processA.add_cpu_burst(4)

    machine.add(processA)

    # process B
    processB = Process.Process("B", 2)

    processB.add_cpu_burst(8)
    processB.add_io_burst(1)
    processB.add_cpu_burst(8)

    machine.add(processB)

    # process C
    processC = Process.Process("C", 3)

    processC.add_cpu_burst(2)
    processC.add_io_burst(1)
    processC.add_cpu_burst(2)

    machine.add(processC)

    # process D
    processD = Process.Process("D", 7)

    processD.add_cpu_burst(1)
    processD.add_io_burst(1)
    processD.add_cpu_burst(1)
    processD.add_io_burst(1)
    processD.add_cpu_burst(1)

    machine.add(processD)

    return machine


