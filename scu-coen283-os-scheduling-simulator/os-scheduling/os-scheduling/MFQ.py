from collections import deque

class MFQ:

    def __init__(self, numLevels, quanta):
        self.numLevels = numLevels
        self.myQueue = [deque()] * numLevels
        self.quanta = quanta
        self.size = 0

    def add(self, item):
        '''
        Adds an item to the multilevel feedback queue
        :param item: item to be added to queue
        :return:
        '''
        # LOWER VALUES OF PRIORITY MEANS HIGHER PRIORITY!

        index = item.priority  # get the priority
        if item.preempted is True:
            index = index + 1  # lower the priority if the item was preempted
        if index >= self.numLevels-1: # if priority is lower than the lowest priority queue, put it in the lowest priority
            item.priority = self.numLevels-1
            item.quantum = self.quanta[self.numLevels-1]
            self.myQueue[self.numLevels-1].append(item)
        else:  # otherwise just put it in the right queue
            self.myQueue[index].append(item)
        self.size += 1

    def get(self):
        '''
        Removes the frontmost element from the highest priority queue and returns it
        :return: frontmost element from highest priority queue
        '''
        for i in range(self.numLevels):  # look through each queue in from highest to lowest priority
            if len(self.myQueue[i]) > 0:  # if the queue i'm looking at isn't empty
                self.size -= 1
                return self.myQueue[i].popleft()  # remove the first item and return it
        return None  # if the whole thing is empty, return None

    def peek(self):
        '''
        Returns the frontmost element from the highest priority queue without removal
        :return: frontmost element from highest priority queue
        '''
        for i in range(self.numLevels):
            if len(self.myQueue[i]) > 0:
                return self.myQueue[i][0]
        return None

    def isEmpty(self):
        '''
        Returns True if structure is empty, False otherwise
        :return: True if structure is empty, False otherwise
        '''
        return self.size == 0

    def isNotEmpty(self):
        '''
        Returns False if structure is empty, True otherwise
        :return: False if structure is empty, True otherwise
        '''
        return self.size > 0

    def toQueue(self):
        '''
        Returns the contents of the structure as a single queue in order from highest priority to lowest priority
        :return: the contents of the structure as a queue
        '''
        result = deque()
        for i in range(self.numLevels):
            result.extend(self.myQueue[i])
        return result
