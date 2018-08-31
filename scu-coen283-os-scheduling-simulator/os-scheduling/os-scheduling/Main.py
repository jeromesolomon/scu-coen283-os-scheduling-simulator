import os
import datetime

import Process
import Machine
import Machine2
import MachineFCFS
import RR
import MFQ
import FirstInFirstOut
import FPPQMachine
import CFS

import PreemptiveMachine
import ScheduleUtilities
import ScheduleTests


#
# Jon's original example
#
"""
machine = Machine.Machine()

process = Process.Process("A", 0)
process.set_by_stats(1, 35, 0, 0, 0)  # makes a process with 1 burst of length 35, no io.
machine.add(process)

process = Process.Process("B", 5)
# makes a process with 1 burst of length 35, no io, enters 5 time units after previous process.
process.set_by_stats(1, 35, 0, 0, 0)
machine.add(process)
"""

#
# Jerome's Test Cases
#

numCores = 1
structure = CFS.CFS(4, 16)  # create the structure for the ready queue

# machine = MachineFCFS.MachineFCFS(numCores)
# machine = MachineRoundRobin.MachineRoundRobin(numCores)

# machine = MachineShortestProcessFirst.MachineShortestProcessFirst(numCores)
# machine = MachineShortestRemainingTimeFirst.MachineShortestRemainingTimeFirst(numCores)
machine = Machine2.Machine2(structure, numCores)  # pass the structure into the machine
# machine = FPPQMachine.FPPQMachine(numCores)


# runs with lecture scheduling data
# ScheduleTests.create_lecture_example(machine, 3)
ScheduleTests.create_CFS_example(machine)
print(len(machine.new))

# multi-core test
# ScheduleTests.create_multi_core_test(machine)
# machine = ScheduleTests.add_test_processes(numCores)

# single process test
# machine = ScheduleTests.create_single_process_test(numCores)

# round robin test
# machine = ScheduleTests.create_round_robin_test(numCores)


# open output data files
csvProcessTraceTableFile = ScheduleUtilities.open_output_file("process_trace_table", "csv")
csvStatsTableFile = ScheduleUtilities.open_output_file("statistics_table", "csv")
csvProcessInfoTableFile = ScheduleUtilities.open_output_file("process_info_table", "csv")

# write the csv header
machine.csv_process_trace_table_write_header(csvProcessTraceTableFile)
machine.csv_statistics_table_write_header(csvStatsTableFile)

#
# start the simulation
#

# print process info table
print(machine.str_process_info_table())

# print machine initial state of machine
print("Initial machine status:")
print(machine)

# write table info file
machine.csv_process_info_table_write(csvProcessInfoTableFile)

# run the machine to completion
print("Running the simulation:")
while machine.process_all():

    # print status of the machine
    print(machine)

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

# print the final machine status
print("Final machine status:")
print(machine)

# print the statistics
machine.print_statistics()

# save the final statistics
machine.csv_statistics_table_write(csvStatsTableFile)

# close the file
csvProcessTraceTableFile.close()
csvStatsTableFile.close()
csvProcessInfoTableFile.close()
