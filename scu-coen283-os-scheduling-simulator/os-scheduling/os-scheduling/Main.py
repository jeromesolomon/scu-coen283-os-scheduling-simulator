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
machine = ScheduleUtilities.create_lecture_example()


print(machine)

# run the machine to completion
while(machine.advance_time()):
    print(machine)

