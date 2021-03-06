import os
import datetime
import random

import Machine
import PreemptiveMachine
import Process
import random

"""
Test functions for schedule toolset
"""

def create_CFS_example(machine):
    processArray = []
    for i in range(5):
        p = Process.Process('p%d' % i, 0, 0)
        if i < 4:
            p.set_by_stats(10, 1, 1, 10, 1)  # make 3 io bound processes
        else:
            p.set_by_stats(4, 20, 5, 3, 1)  # make 2 cpu-bound processes

        p.priority = i if i < 3 else 3

        processArray.append(p)
        print(p)
    random.shuffle(processArray)
    startTime = 0
    pid = 100
    for p in processArray:
        p.startTime = startTime
        p.id = pid
        startTime += 2
        pid += 1
        machine.add(p)
    return machine

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
    processA = Process.Process("A", 0, quantum, priority=5)

    processA.add_cpu_burst(4)
    processA.add_io_burst(4)
    processA.add_cpu_burst(4)
    processA.add_io_burst(4)
    processA.add_cpu_burst(4)

    machine.add(processA)

    # process B
    processB = Process.Process("B", 2, quantum, priority=10)

    processB.add_cpu_burst(8)
    processB.add_io_burst(1)
    processB.add_cpu_burst(8)

    machine.add(processB)

    # process C
    processC = Process.Process("C", 3, quantum, priority=1)

    processC.add_cpu_burst(2)
    processC.add_io_burst(1)
    processC.add_cpu_burst(2)

    machine.add(processC)

    # process D
    processD = Process.Process("D", 7, quantum, priority=0)

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


def create_balanced_process(name, startTime, quantum):

    process = Process.Process(name, startTime, quantum)
    cpuTotal = 0
    ioTotal = 0

    numBursts = random.randint(1, 10)
    for i in range(0, numBursts):

        cpu = random.randint(1, 10)
        process.add_cpu_burst(cpu)
        cpuTotal += cpu

        io = random.randint(1, 5)
        process.add_io_burst(io)
        ioTotal += io
    process.priority = 20 * cpuTotal / (cpuTotal + ioTotal)  # define priority to be proportional to cpu time %
    return process


def create_balanced_statistical_test(machine, numProcesses):

    quantum = 3
    startTime = 0

    for i in range(0, numProcesses):
        process = create_balanced_process("A" + str(i), startTime, quantum)
        machine.add(process)


def create_cpu_heavy_process(name, startTime, quantum):

    process = Process.Process(name, startTime, quantum)
    cpuTotal = 0
    ioTotal = 0

    numBursts = random.randint(1, 10)
    for i in range(0, numBursts):

        cpu = random.randint(1, 10)
        process.add_cpu_burst(cpu)
        cpuTotal += cpu

        io = random.randint(1, 1)
        process.add_io_burst(io)
        ioTotal += io
    process.priority = 20 * cpuTotal / (cpuTotal + ioTotal)  # define priority to be proportional to cpu time %
    return process


def create_cpu_heavy_statistical_test(machine, numProcesses):

    quantum = 3
    startTime = 0

    for i in range(0, numProcesses):
        process = create_cpu_heavy_process("A" + str(i), startTime, quantum)
        machine.add(process)


def create_io_heavy_process(name, startTime, quantum):

    process = Process.Process(name, startTime, quantum)
    cpuTotal = 0
    ioTotal = 0

    numBursts = random.randint(1, 10)
    for i in range(0, numBursts):

        cpu = random.randint(1, 1)
        process.add_cpu_burst(cpu)
        cpuTotal += cpu

        io = random.randint(1, 10)
        process.add_io_burst(io)
        ioTotal += io
    process.priority = 20 * cpuTotal / (cpuTotal + ioTotal)  # define priority to be proportional to cpu time %
    return process


def create_io_heavy_statistical_test(machine, numProcesses):

    quantum = 3
    startTime = 0

    for i in range(0, numProcesses):
        process = create_io_heavy_process("A" + str(i), startTime, quantum)
        machine.add(process)

def create_cpu_only_process(name, startTime, quantum):

    process = Process.Process(name, startTime, quantum)

    numBursts = random.randint(1, 10)
    for i in range(0, numBursts):

        cpu = random.randint(1, 20)
        process.add_cpu_burst(cpu)

    return process


def create_cpu_only_statistical_test(machine, numProcesses):

    quantum = 3
    startTime = 0

    for i in range(0, numProcesses):
        process = create_cpu_only_process("A" + str(i), startTime, quantum)
        machine.add(process)