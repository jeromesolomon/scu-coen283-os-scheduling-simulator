import Process
import Machine

machine = Machine.Machine()
l = list()

#
# Professor Elkady's class lecture example
#

# process A
processA = Process.Process("A", 0)

processA.addcpuburst(4)
processA.addioburst(4)
processA.addcpuburst(4)
processA.addioburst(4)
processA.addcpuburst(4)

machine.add(processA)

# process B
processB = Process.Process("B", 2)

processB.addcpuburst(8)
processB.addioburst(1)
processB.addcpuburst(8)

machine.add(processB)

# process C
processC = Process.Process("C", 3)

processC.addcpuburst(2)
processC.addioburst(1)
processC.addcpuburst(2)

machine.add(processC)

# process D
processD = Process.Process("D", 7)

processD.addcpuburst(1)
processD.addioburst(1)
processD.addcpuburst(1)
processD.addioburst(1)
processD.addcpuburst(1)

machine.add(processD)


""" Jon's original example
process = Process.Process("A",0)
process.setbystats(1, 35, 0, 0, 0)  # makes a process with 1 burst of length 35, no io.
machine.add(process)


process = Process.Process("B",5)
process.setbystats(1, 35, 0, 0, 0)  # makes a process with 1 burst of length 35, no io, enters 5 time units after previous process.
machine.add(process)
"""

print(machine)

while(machine.advanceTime()):
    print(machine)
print(machine)
