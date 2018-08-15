import Process
import Machine
import ScheduleUtilities


#
# Jon's original example
#

"""
machine = Machine.Machine()


process = Process.Process("A", 0)
process.setbystats(1, 35, 0, 0, 0)  # makes a process with 1 burst of length 35, no io.
machine.add(process)


process = Process.Process("B", 5)
process.setbystats(1, 35, 0, 0, 0)  # makes a process with 1 burst of length 35, no io, enters 5 time units after previous process.
machine.add(process)

"""

# runs with lecture scheduling data
#machine = ScheduleUtilities.create_lecture_example()

# multi-core test
machine = ScheduleUtilities.create_multi_core_test()
ScheduleUtilities.add_test_processes(machine)

print(machine)

for i in range(0, 5):

    # process all the queues
    hasProcesses = machine.process_all_queues()

    # print status of the machine
    print(machine)

    # if cpu has processes in new, ready, blocked, or cpu, increase time by 1
    if hasProcesses:
        machine.time += 1


# run the machine to completion
"""
hasProcesses = True
while(hasProcesses):
    # process all the queues
    hasProcesses = machine.process_all_queues()

    # print status of the machine
    print(machine)

    # if cpu has processes in new, ready, blocked, or cpu, increase time by 1
    if hasProcesses:
        machine.time += 1
"""

