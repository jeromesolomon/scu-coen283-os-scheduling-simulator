import Process
import Machine
from collections import deque

class FIFO:

    def __init__(self):
        self.myQueue = deque()
        self.size = 0

    def __str__(self):
        """
        Private method used to print a queue neatly.
        :return: a string
        """
        mystring = ""
        if len(self.myQueue) == 0:
            mystring += "\t" + "<empty>" + "\n"
        else:
            for p in self.myQueue:
                mystring += "\t" + str(p) + "\n"

        return mystring


    def add(self, item):
        """
        Method to add an item to the queue
        :param item: item to be added
        :return:
        """
        self.myQueue.append(item)
        self.size += 1

    def get(self):
        """
        Method to remove an item from the queue and return it
        :return: frontmost item in queue
        """
        if self.isEmpty():
            return None
        self.size -=1
        return self.myQueue.popleft()

    def peek(self):
        """
        Method to return the frontmost item from the queue without removal
        :return: frontmost item in queue
        """
        return self.myQueue[0]

    def isEmpty(self):
        """
        Method to return whether the structure is empty
        :return: True if structure is empty, False otherwise
        """
        return len(self.myQueue) == 0

    def isNotEmpty(self):
        """
         Method to return whether the structure is not empty
        :return: False if structure is empty, True otherwise
        """
        return len(self.myQueue) > 0

    def toQueue(self):
        """
        Method to "queueify" the structure
        :return: The items in the structure as a queue
        """
        return self.myQueue
