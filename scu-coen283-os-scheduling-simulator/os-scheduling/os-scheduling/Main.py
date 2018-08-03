import Process
import Machine

machine = Machine.Machine()
l = list()
for i in range(2):
    if i == 0:
        process = Process.Process(i, 1, 35, 0, 0, 0, 0)
    else:
        process = Process.Process(i, 1, 35, 0, 0, 0, 5)
    machine.add(process)

print(machine)
while(machine.advanceTime()):
    print(machine)
print(machine)
