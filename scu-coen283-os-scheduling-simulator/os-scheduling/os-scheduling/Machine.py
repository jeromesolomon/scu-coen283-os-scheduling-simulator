import from collections deque


class Machine:

    machineTime = 0
    new = deque()
    ready = deque()
    running = None
    blocked = deque()

    def add(process):
        new.append(process)

    def advanceTime():
        # returns False if time was not advanced, True if it was
        # newTime is the time until arrival
        newTime = machineTime - new[0].getTime() if len(new) > 0 else None
        runningTime = None if running == None else running.getTime()
        blockedTime = None if len(blocked) == 0 else blocked[0].getTime()
        times = list()

        if(newTime != None):
            times.append(newTime)
        if(runningTime != None):
            times.append(runningTime)
        if(blockedTime != None):
            times.append(blockedTime)

        if(len(times) == 0)
            return False  # this means that the new queue is empty, the running state is empty, and the blocked queue is empty

        delta = min(times)

        if len(new) > 0 and new[0].decrement(delta):
            # if there is a new process and this time advancement zeroes out the delay of the frontmost process
            ready.append(new.popleft())  # take process from new and put it into ready

        if running != None and running.decrement(delta):
            # if there is something running and this time advancement zeroes out its burst time
            blocked.append(running)  # it's blocked now (internal flagging happened already)
            running = None  # set running to None first
            if(len(ready) > 0):  # if there's something to be run
                running = ready.popleft()  # put it into the running spot

        if len(ready) > 0 and running == None:  # if there's something ready and nothing running
            running = ready.popleft()  # take the frontmost element out of the ready queue and put it into the running spot

        if len(blocked) > 0 and blocked[0].decrement(delta):
            # if there is something blocked and this time advancement zeroes out the wait time of the frontmost process
            ready.append(blocked.popleft())  # dequeue from blocked and enqueue into ready

        return True  # do this at the end because two of the above blocks may execute during the same time slice
