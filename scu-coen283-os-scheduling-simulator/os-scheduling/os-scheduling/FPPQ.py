import heapq
class FPPQ:
    def __init__(self):
        self.heap = []
        self.size = 0
        self.preemptionQueue = []

    def add(self, item):
        '''
        Adds process to the structure
        :param item: the process to be added
        :return:
        '''
        item.quantum = item.bursts[0][1]
        itemtuple = (item.priority, item.id, item)
        heapq.heappush(self.heap, itemtuple)
        self.size += 1


    def get(self):
        '''
        Gets the next process to run.
        :return: the next available process
        '''
        result = None

        if len(self.preemptionQueue) > 0:
            result = self.preemptionQueue.popLeft()
        if self.size > 0:
            priority, id, result = heapq.heappop(self.heap)
            self.size -= 1
        return result

    def preempt(self, item):
        '''
        Returns whether there is a process with higher priority in the queue
        :param item: the process to compare against
        :return: True if queue contains higher priority tasks than
        '''

        preempt = item.priority > self.peek().priority
        if preempt is True:
            self.preemptionQueue.append(self.get())

        return item.priority > self.peek().priority

    def peek(self):
        return self.heap[0][2]

    def isEmpty(self):
        return self.size == 0

    def isNotEmpty(self):
        return self.size > 0

    def toQueue(self):
        result = []
        for x in self.heap:
            priority, id, process = x
            if process is not None:
                result.append(process)

        return result