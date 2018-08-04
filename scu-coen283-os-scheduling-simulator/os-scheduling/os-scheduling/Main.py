import Process
import Machine

machine = Machine.Machine()
l = list()
for i in range(2):
    if i == 0:
        process = Process.Process(i, 1, 35, 0, 0, 0, 0)  # makes a process with 1 burst of length 35, no io.
    else:
        process = Process.Process(i, 1, 35, 0, 0, 0, 5)  # makes a process with 1 burst of length 35, no io, enters 5 time units after previous process.
    machine.add(process)

print(machine)
while(machine.advanceTime()):
    print(machine)
print(machine)
