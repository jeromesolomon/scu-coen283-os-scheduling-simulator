import Process
import Machine
import ScheduleUtilities


#
# Jon's original example
#
machine = Machine.Machine()

"""
process = Process.Process("A", 0)
process.set_by_stats(1, 35, 0, 0, 0)  # makes a process with 1 burst of length 35, no io.
machine.add(process)

process = Process.Process("B", 5)
process.set_by_stats(1, 35, 0, 0, 0)  # makes a process with 1 burst of length 35, no io, enters 5 time units after previous process.
machine.add(process)
"""

#
# Jerome's Test Cases
#

# runs with lecture scheduling data
machine = ScheduleUtilities.create_lecture_example()

# multi-core test
# machine = ScheduleUtilities.create_multi_core_test()
# ScheduleUtilities.add_test_processes(machine)

# single process test
# machine = ScheduleUtilities.create_single_process_test()

# open a csv file for saving & viewing the simulation in excel
csvFileName = "simulation_output"
try:
    csvFile = open(csvFileName + ".csv", "w")
except IOError:
    print("ERROR: opening the file " + csvFileName)
    exit(-1)

# write the csv header
machine.csv_write_header(csvFile)

# print machine initial state of machine
print("Initial machine status:")
print(machine)
 
# run the machine to completion
print("Running the simulation:")
while machine.process_all():

    # print status of the machine
    print(machine)

    # write a line to the csv file
    machine.csv_write(csvFile)

    # save machine data to csv
    
    # calculate statistics
    machine.calculate_statistics()
    
    # process stage2 io
    machine.process_io_stage2()

    # increase time
    machine.time += 1
    
# print the final machine status
print("Final machine status:")
print(machine)

# print the statistics
machine.print_statistics()

# close the file
csvFile.close()



