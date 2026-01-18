import heapq
from collections import defaultdict

class RunningMedian:
    def __init__(self):
        # Two heaps
        self.max_heap = []  # Max heap to store the upper half of the numbers
        self.min_heap = []  # Min heap to store the lower half of the numbers

    def add_number(self, num):
        # Add to max heap
        heapq.heappush(self.max_heap, -num)

        # Balance heaps
        heapq.heappush(self.min_heap, -heapq.heappop(self.max_heap))

        if len(self.max_heap) < len(self.min_heap):
            heapq.heappush(self.max_heap, -heapq.heappop(self.min_heap))

    def get_median(self):
        if len(self.max_heap) == len(self.min_heap):
            return (-self.max_heap[0] + self.min_heap[0]) / 2.0
        else:
            return -self.max_heap[0]

# Simulate the stream processing with a list of numbers as an example
numbers = [5, 15, 1, 3]
running_median = RunningMedian()
for num in numbers:
    running_median.add_number(num)
    print("Running median so far:", running_median.get_median())