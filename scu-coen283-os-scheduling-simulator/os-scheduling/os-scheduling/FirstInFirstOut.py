import Process
import Machine
from collections import deque

class FIFO:

    def __init__(self):
        self.myQueue = deque()

    def add(self, item):
        self.myQueue.append(item)

    def get(self):
        return self.myQueue.popleft()

    def peek(self):
        return self.myQueue[0]

    def isEmpty(self):
        return len(self.myQueue) == 0

