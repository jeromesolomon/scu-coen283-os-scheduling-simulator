import os
import datetime

import Process
import Machine
import MachineFCFS
import MachineRoundRobin
import MachineShortestProcessFirst
import MachineShortestRemainingTimeFirst
import ScheduleUtilities
import ScheduleTests


def run_simulation(machine, algorithmName, numCores, numProcesses):
    """
    runs a scheduling algorithm simulation
    :param machine: the machine/algorithm
    :param testName: the name of the test
    :return:
    """

    # open output data files
    prefix = algorithmName + "_" + str(numCores) + "cores" + "_" + str(numProcesses) + "processes" + "_"
    csvProcessTraceTableFile = ScheduleUtilities.open_output_file(algorithmName, prefix + "process_trace_table", "csv")
    csvStatsTableFile = ScheduleUtilities.open_output_file(algorithmName, prefix + "statistics_table", "csv")
    csvProcessInfoTableFile = ScheduleUtilities.open_output_file(algorithmName, prefix + "process_info_table", "csv")

    # write the csv header
    machine.csv_process_trace_table_write_header(csvProcessTraceTableFile)
    machine.csv_statistics_table_write_header(csvStatsTableFile)

    #
    # start the simulation
    #

    # print process info table
    # print(machine.str_process_info_table())

    # print machine initial state of machine
    # print("Initial machine status:")
    # print(machine)

    # write table info file
    machine.csv_process_info_table_write(csvProcessInfoTableFile)

    # run the machine to completion
    print("Running the simulation")

    while machine.process_all():

        # print status of the machine
        # print(machine)

        # write a status line to the csv file
        machine.csv_process_trace_table_write(csvProcessTraceTableFile)

        # calculate statistics
        machine.calculate_statistics()

        # write statistics
        machine.csv_statistics_table_write(csvStatsTableFile)

        # process stage2 io
        machine.process_io_stage2()

        # increase time
        machine.time += 1

    print("Simulation done.")
    # print the final machine status
    # print("Final machine status:")
    # print(machine)

    # print the statistics
    machine.print_statistics()

    # save the final statistics
    machine.csv_statistics_table_write(csvStatsTableFile)

    # close the file
    csvProcessTraceTableFile.close()
    csvStatsTableFile.close()
    csvProcessInfoTableFile.close()


#
# MAIN
#

# various type of core configurations
numCoresList = [1, 2, 4]

# number of processes in each sim
numProcessesList = [4, 8, 16] # for statistical example
numProcessesList = [1] # for lecture example since it is defined within the lecture example

# number of type of schedule algorithms
typeMachinesList = ["fcfs", "roundrobin", "spf", "srtf"]
numTypeMachines = len(typeMachinesList)

# 3 dimensional array
machineMatrix = [[[None for k in range(len(numProcessesList))] for j in range(len(numCoresList))] for i in range(len(typeMachinesList))]

#print(machineMatrix)

"""
for i in range(len(typeMachinesList)):
    for j in range(len(numCoresList)):
        for k in range(len(numProcessesList)):
            print(machineMatrix[i][j][k])
"""

#
# create all the machines and add them to the matrix
#
for j in range(0, len(numCoresList)):
    for k in range(0, len(numProcessesList)):

        # add machines of each type to the matrix

        # FCFS
        machineMatrix[0][j][k] = MachineFCFS.MachineFCFS(numCoresList[j])

        # Round Robin
        machineMatrix[1][j][k] = MachineRoundRobin.MachineRoundRobin(numCoresList[j])

        # SPF
        machineMatrix[2][j][k] = MachineShortestProcessFirst.MachineShortestProcessFirst(numCoresList[j])

        # SRTF
        machineMatrix[3][j][k] = MachineShortestRemainingTimeFirst.MachineShortestRemainingTimeFirst(numCoresList[j])

#print(machineMatrix)

#
# create process test cases
#
for j in range(0, len(numCoresList)):
    for k in range(0, len(numProcessesList)):

        ScheduleTests.create_lecture_example(machineMatrix[0][j][k], 3)
        ScheduleTests.create_lecture_example(machineMatrix[1][j][k], 3)
        ScheduleTests.create_lecture_example(machineMatrix[2][j][k], 3)
        ScheduleTests.create_lecture_example(machineMatrix[3][j][k], 3)

        """
        ScheduleTests.create_statistical_test(machineMatrix[0][j][k], numProcessesList[k])
        ScheduleTests.create_statistical_test(machineMatrix[1][j][k], numProcessesList[k])
        ScheduleTests.create_statistical_test(machineMatrix[2][j][k], numProcessesList[k])
        ScheduleTests.create_statistical_test(machineMatrix[3][j][k], numProcessesList[k])
        """


# runs with lecture scheduling data
# ScheduleTests.create_lecture_example(machine, 3)
# ScheduleTests.create_statistical_test(machine, 8)

#
# run all the simulations
#
for i in range(len(typeMachinesList)):
    for j in range(len(numCoresList)):
        for k in range(len(numProcessesList)):

            simName = ""
            simName += "Running simulation with: "
            simName += typeMachinesList[i]
            simName += " # of cores = " + str(numCoresList[j])
            simName += " # of processes  = " + str(numProcessesList[k])
            print(simName)

            algorithmName = typeMachinesList[i]
            numCores = numCoresList[j]
            numProcesses = numProcessesList[k]

            run_simulation(machineMatrix[i][j][k], algorithmName, numCores, numProcesses)
