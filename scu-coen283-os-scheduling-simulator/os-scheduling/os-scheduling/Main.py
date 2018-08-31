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


def run_simulation(machine, testName):
    """
    runs a scheduling algorithm simulation
    :param machine: the machine/algorithm
    :param testName: the name of the test
    :return:
    """

    # open output data files
    csvProcessTraceTableFile = ScheduleUtilities.open_output_file(testName + "_process_trace_table", "csv")
    csvStatsTableFile = ScheduleUtilities.open_output_file(testName + "_statistics_table" + testName, "csv")
    csvProcessInfoTableFile = ScheduleUtilities.open_output_file(testName + "_process_info_table", "csv")

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
    print("Running the simulation " + testName)

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
numCoreList = [1, 8, 72]

# number of processes in each sim
numProcessesList = [4, 500, 5000]

# number of type of schedule algorithms
typeMachinesList = ["FCFS", "RoundRobin", "SPF", "SRTF"]
numTypeMachines = len(typeMachinesList)

matrix = [[[0 for i in range(len(typeMachinesList))] for j in range(len(numCoreList))] for k in range(len(numProcessesList))]

# create machines
for numProcess in numProcessesList:
    for i in range(0, len(numCoreList)):

    machineListFCFS.append(MachineFCFS.MachineFCFS(numCore))
    machineListRoundRobin.append(MachineRoundRobin.MachineRoundRobin(numCore))
    machineListSPF.append(MachineShortestProcessFirst.MachineShortestProcessFirst(numCore))
    machineListSRTF.append(MachineShortestRemainingTimeFirst.MachineShortestRemainingTimeFirst(numCore))

# create process test cases
for numProcess in numProcessesList:
    for i in range(0, len(numCoreList)):
        ScheduleTests.create_delivery_test(machineListFCFS[i], numProcess)
        ScheduleTests.create_delivery_test(machineListRoundRobin[i], numProcess)
        ScheduleTests.create_delivery_test(machineListSPF[i], numProcess)
        ScheduleTests.create_delivery_test(machineListSRTF[i], numProcess)

# runs with lecture scheduling data
# ScheduleTests.create_lecture_example(machine, 3)
# ScheduleTests.create_delivery_test(machine, 500)

# create process test cases
for numProcess in numProcessesList:
    for i in range(0, len(numCoreList)):
        run_simulation(machineListFCFS[i], "FCFS_" + "processes_" + str(numProcess) + "_cores_" + str(numCoreList[i]))

