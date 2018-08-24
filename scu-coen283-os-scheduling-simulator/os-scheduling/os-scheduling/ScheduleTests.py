import os
import datetime

import Machine
import Process

"""
Test functions for schedule toolset
"""

def create_lecture_example(machine, quantum):
    """
    Creates the example of four processes from Professor Amr Elkady's lecture
    :return: returns a machine with the lecture example processes
    """

    #
    # Professor Amr Elkady's class lecture example
    #

    quantum = 3

    # process A
    processA = Process.Process("A", 0, quantum)

    processA.add_cpu_burst(4)
    processA.add_io_burst(4)
    processA.add_cpu_burst(4)
    processA.add_io_burst(4)
    processA.add_cpu_burst(4)

    machine.add(processA)

    # process B
    processB = Process.Process("B", 2, quantum)

    processB.add_cpu_burst(8)
    processB.add_io_burst(1)
    processB.add_cpu_burst(8)

    machine.add(processB)

    # process C
    processC = Process.Process("C", 3, quantum)

    processC.add_cpu_burst(2)
    processC.add_io_burst(1)
    processC.add_cpu_burst(2)

    machine.add(processC)

    # process D
    processD = Process.Process("D", 7, quantum)

    processD.add_cpu_burst(1)
    processD.add_io_burst(1)
    processD.add_cpu_burst(1)
    processD.add_io_burst(1)
    processD.add_cpu_burst(1)

    machine.add(processD)

    return machine


def create_multi_core_test(machine):

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


def add_test_processes(m):

    p = Process.Process("TEST-NO-BURST", 3)
    m.add(p)

    p = Process.Process("TEST-CPU-ONLY", 3)
    p.add_cpu_burst(3)
    p.add_cpu_burst(3)
    m.add(p)

    p = Process.Process("TEST-IO-ONLY", 3)
    p.add_io_burst(3)
    p.add_io_burst(3)
    m.add(p)

    p = Process.Process("TEST-UNORDERED", 3)
    p.add_io_burst(3)
    p.add_cpu_burst(3)
    p.add_cpu_burst(3)
    p.add_io_burst(3)
    m.add(p)


def create_single_process_test(machine):

    p = Process.Process("Single-Process", 0)

    p.add_cpu_burst(3)
    p.add_io_burst(3)
    p.add_cpu_burst(2)
    p.add_io_burst(2)
    p.add_cpu_burst(1)

    machine.add(p)

    return machine


def create_round_robin_test(machine, quantum):
    """
    Creates the example of four processes from Professor Amr Elkady's lecture
    :return: returns a machine with the lecture example processes
    """

    #
    # Professor Amr Elkady's class lecture example
    #

    # process A
    processA = Process.Process("A", 0, quantum)

    processA.add_cpu_burst(4)
    processA.add_io_burst(4)
    processA.add_cpu_burst(4)
    processA.add_io_burst(4)
    processA.add_cpu_burst(4)

    machine.add(processA)

    # process B
    processB = Process.Process("B", 2, quantum)

    processB.add_cpu_burst(8)
    processB.add_io_burst(1)
    processB.add_cpu_burst(8)

    machine.add(processB)

    return machine
