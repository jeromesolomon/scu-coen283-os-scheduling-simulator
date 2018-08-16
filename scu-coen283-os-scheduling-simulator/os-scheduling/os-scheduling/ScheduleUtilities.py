import Machine
import Process

"""
Utility functions for schedule toolset
"""


def createlectureexample():
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

    processA.addcpuburst(4)
    processA.addioburst(4)
    processA.addcpuburst(4)
    processA.addioburst(4)
    processA.addcpuburst(4)

    machine.add(processA)

    # process B
    processB = Process.Process("B", 2)

    processB.addcpuburst(8)
    processB.addioburst(1)
    processB.addcpuburst(8)

    machine.add(processB)

    # process C
    processC = Process.Process("C", 3)

    processC.addcpuburst(2)
    processC.addioburst(1)
    processC.addcpuburst(2)

    machine.add(processC)

    # process D
    processD = Process.Process("D", 7)

    processD.addcpuburst(1)
    processD.addioburst(1)
    processD.addcpuburst(1)
    processD.addioburst(1)
    processD.addcpuburst(1)

    machine.add(processD)

    return machine


