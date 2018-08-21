from collections import deque

class MFQ:

    def __init__(self, numLevels):
        self.numLevels = numLevels
        self.myQueue = [deque()] * numLevels
        self.front = [None] * numLevels
        self.size = 0

    def add(self, item):
        #get the priority
        index = item.priority

        if index >= self.numLevels-1: #if priority is lower than the lowest priority queue, put it in the lowest priority
            item.priority = self.numLevels-1
            self.myQueue[self.numLevels-1].append(item)
        else:  #otherwise just put it in the right queue
            self.myQueue[index].append(item)
        self.size += 1

    def get(self):
        #fill this out
        return None

    def peek(self):
        #fill this out
        return None

    def isEmpty(self):
        #fill this out
        return None

    def isNotEmpty(self):



    def toQueue(self):
        return self.myQueue