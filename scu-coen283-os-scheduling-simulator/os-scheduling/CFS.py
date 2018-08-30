import heapq

class CFS:

    def __init__(self, maxpriority, timeSliceSize):
        self.heap = []
        self.maxpriority = maxpriority
        self.middlepriority = maxpriority // 2
        self.size = 0
        self.timeSliceSize = timeSliceSize
        self.totalweight = 0

    def calcDelta(self, item):
        return round(item.cputime * (2**(self.middlepriority - self.maxpriority)))

    def calcvruntime(self, item):
        if item.vruntime is None:
            if len(self.heap) == 0:
                item.vruntime = 0
            else:
                item.vruntime = self.heap[0][0]
        else:
            item.vruntime = item.vruntime + self.calcDelta(item)

        return item.vruntime

    def calcweight(self, item):
        return 2**(self.maxpriority - item.priority)

    def add(self, item):
        self.calcvruntime(item)
        heapq.heappush((self.calcvruntime(item), item))  # push the item into the heap
        item.cputime = 0  # reset cpu time for the process after it's used
        self.size += 1
        self.totalweight += self.calcweight(item)

    def get(self):
        result = None
        if self.size > 0:
            result = heapq.heappop(self.heap)[1]
            result.quantum = round(self.timeSliceSize * self.calcweight(result) / self.totalweight)
            self.size -= 1
            self.totalweight -= self.calcweight(result)
        return result

    def peek(self):
        return self.heap[0][1]

    def isEmpty(self):
        return self.size == 0

    def isNotEmpty(self):
        return self.size > 0

    def toQueue(self):
        return self.heap
