from collections import deque

class MFQ:

    def __init__(self, structureList):
        self.numLevels = len(structureList)
        self.structureList = structureList
        self.size = 0

    def add(self, item):
        '''
        Adds an item to the multilevel feedback queue
        :param item: item to be added to queue
        :return:
        '''
        # LOWER VALUES OF PRIORITY MEANS HIGHER PRIORITY!

        index = item.priority  # get the priority
        if item.preempt is True:
            index = max(index + 1, self.numLevels-1)  # lower the priority if the item was preempted, up to numLevels-1
        else:
            index = min(index - 1, 0) # raise the priority if not preempted, down to 0

        # 0 <= index <= self.numLevels-1

        self.structureList[index].add(item)
        self.size += 1

    def get(self):
        '''
        Removes the frontmost element from the highest priority queue and returns it
        :return: frontmost element from highest priority queue
        '''
        for i in range(self.numLevels):  # look through each queue in from highest to lowest priority
            if self.structureList[i].size > 0:  # if the queue i'm looking at isn't empty
                self.size -= 1
                return self.structureList[i].get()  # remove the first item and return it
        return None  # if the whole thing is empty, return None

    def peek(self):
        '''
        Returns the frontmost element from the highest priority queue without removal
        :return: frontmost element from highest priority queue
        '''
        for i in range(self.numLevels):
            if self.structureList[i].size > 0:
                return self.structureList[i].peek()
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
            result.extend(self.structureList[i].toQueue())
        return result
