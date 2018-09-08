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

# set of this variable to try to run that appropriate workload
# lecture = prof. elkady's lecture example
# balanced = statistical example with a balanced mixed cpu and io
# cpu_heavy = statistical example with heavy cpu and little io
# io_heavy = statistical example with little cpu and heavy io
# cpu_only = statistical example with no io (just one big cpu burst)
gWorkloadType = "lecture"

# write csv files for each algorithm (can use a lot of disk space)
gDebugCSVFiles = True

# print detailed debug messages
gDebugPrint = False

def run_simulation(machine, algorithmName, numCores, numProcesses):
    """
    runs a scheduling algorithm simulation
    :param machine: the machine/algorithm
    :param testName: the name of the test
    :return:
    """

    # open output data files
    prefix = algorithmName + "_" + str(numCores) + "cores" + "_" + str(numProcesses) + "processes" + "_"

    if gDebugCSVFiles:
        # open file
        csvProcessTraceTableFile = ScheduleUtilities.open_output_file(algorithmName, prefix + "process_trace_table", "csv", "w")
        csvStatsTableFile = ScheduleUtilities.open_output_file(algorithmName, prefix + "statistics_table", "csv", "w")
        csvProcessInfoTableFile = ScheduleUtilities.open_output_file(algorithmName, prefix + "process_info_table", "csv", "w")

    if gDebugCSVFiles:
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

    if gDebugCSVFiles:
        # write table info file
        machine.csv_process_info_table_write(csvProcessInfoTableFile)

    while machine.process_all():

        # print status of the machine
        if gDebugPrint:
            print(machine)

        if gDebugCSVFiles:
            # write a status line to the csv file
            machine.csv_process_trace_table_write(csvProcessTraceTableFile)

        # calculate statistics
        machine.calculate_statistics()

        if gDebugCSVFiles:
            # write statistics
            machine.csv_statistics_table_write(csvStatsTableFile)

        # process stage2 io
        machine.process_io_stage2()

        # increase time
        machine.time += 1

    if gDebugPrint:
        print("Simulation done.")
        # print the final machine status
        # print("Final machine status:")
        # print(machine)

    if gDebugPrint:
        # print the statistics
        machine.print_statistics()

    if gDebugCSVFiles:
        # save the final statistics
        machine.csv_statistics_table_write(csvStatsTableFile)

    if gDebugCSVFiles:
        # close the output files
        csvProcessTraceTableFile.close()
        csvStatsTableFile.close()
        csvProcessInfoTableFile.close()


#
# MAIN
#

# open all statistics file, appending to the end of it
dirName = gWorkloadType + "_all"
fileName = gWorkloadType + "_all_statistics_table"
csvAllStatsTableFile = ScheduleUtilities.open_output_file(dirName, fileName, "csv", "a")

# write the header for the all statistics file
temp = MachineFCFS.MachineFCFS()
temp.csv_all_statistics_table_write_header(csvAllStatsTableFile)

# various type of core configurations
if gWorkloadType == "lecture":
    numCoresList = [1, 2, 4]
    numProcessesList = [4]

if gWorkloadType == "balanced":
    numCoresList = [1, 2, 4, 8, 16, 24, 32, 48]
    numProcessesList = [10, 100, 500, 1000]

if gWorkloadType == "cpu_heavy":
    numCoresList = [1, 2, 4, 8, 16, 24, 32, 48]
    numProcessesList = [10, 100, 500, 1000]

if gWorkloadType == "io_heavy":
    numCoresList = [1, 2, 4, 8, 16, 24, 32, 48]
    numProcessesList = [10, 100, 500, 1000]

if gWorkloadType == "cpu_only":
    numCoresList = [1, 2, 4, 8, 16, 24, 32, 48]
    numProcessesList = [10, 100, 500, 1000]

# the type of schedule algorithms
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

        if gWorkloadType == "lecture":
            ScheduleTests.create_lecture_example(machineMatrix[0][j][k], 3)
            ScheduleTests.create_lecture_example(machineMatrix[1][j][k], 3)
            ScheduleTests.create_lecture_example(machineMatrix[2][j][k], 3)
            ScheduleTests.create_lecture_example(machineMatrix[3][j][k], 3)

        if gWorkloadType == "balanced":
            ScheduleTests.create_balanced_statistical_test(machineMatrix[0][j][k], numProcessesList[k])
            ScheduleTests.create_balanced_statistical_test(machineMatrix[1][j][k], numProcessesList[k])
            ScheduleTests.create_balanced_statistical_test(machineMatrix[2][j][k], numProcessesList[k])
            ScheduleTests.create_balanced_statistical_test(machineMatrix[3][j][k], numProcessesList[k])

        if gWorkloadType == "cpu_heavy":
            ScheduleTests.create_cpu_heavy_statistical_test(machineMatrix[0][j][k], numProcessesList[k])
            ScheduleTests.create_cpu_heavy_statistical_test(machineMatrix[1][j][k], numProcessesList[k])
            ScheduleTests.create_cpu_heavy_statistical_test(machineMatrix[2][j][k], numProcessesList[k])
            ScheduleTests.create_cpu_heavy_statistical_test(machineMatrix[3][j][k], numProcessesList[k])

        if gWorkloadType == "io_heavy":
            ScheduleTests.create_io_heavy_statistical_test(machineMatrix[0][j][k], numProcessesList[k])
            ScheduleTests.create_io_heavy_statistical_test(machineMatrix[1][j][k], numProcessesList[k])
            ScheduleTests.create_io_heavy_statistical_test(machineMatrix[2][j][k], numProcessesList[k])
            ScheduleTests.create_io_heavy_statistical_test(machineMatrix[3][j][k], numProcessesList[k])

        if gWorkloadType == "cpu_only":
            ScheduleTests.create_cpu_only_statistical_test(machineMatrix[0][j][k], numProcessesList[k])
            ScheduleTests.create_cpu_only_statistical_test(machineMatrix[1][j][k], numProcessesList[k])
            ScheduleTests.create_cpu_only_statistical_test(machineMatrix[2][j][k], numProcessesList[k])
            ScheduleTests.create_cpu_only_statistical_test(machineMatrix[3][j][k], numProcessesList[k])

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
            simName += "Running simulation: "
            simName += gWorkloadType + "_"
            simName += typeMachinesList[i]
            simName += " with # of cores = " + str(numCoresList[j])
            simName += " and # of processes  = " + str(numProcessesList[k])
            print(simName)

            algorithmName = gWorkloadType + "_" + typeMachinesList[i]
            numCores = numCoresList[j]
            numProcesses = numProcessesList[k]

            # run the simulation
            run_simulation(machineMatrix[i][j][k], algorithmName, numCores, numProcesses)

            # write out the all statistics file, append the final statistics to the all statistics table
            machineMatrix[i][j][k].csv_all_statistics_table_write( \
                csvAllStatsTableFile, algorithmName, numCores, numProcesses)

# close the all statistics file
csvAllStatsTableFile.close()
