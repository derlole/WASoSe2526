import heapq

class RunningMedian:
    def __init__(self):
        self.min_heap = []  # Max-heap to store the lower half of the numbers
        self.max_heap = []  # Min-heap to store the upper half of the numbers

    def add_num(self, num):
        if not self.min_heap or num <= -self.min_heap[0]:
            heapq.heappush(self.min_heap, -num)
        else:
            heapq.heappush(self.max_heap, num)

        # Balance the heaps
        if len(self.min_heap) > len(self.max_heap) + 1:
            heapq.heappush(self.max_heap, -heapq.heappop(self.min_heap))
        elif len(self.max_heap) > len(self.min_heap):
            heapq.heappush(self.min_heap, -heapq.heappop(self.max_heap))

    def get_median(self):
        if len(self.min_heap) == len(self.max_heap):
            return (-self.min_heap[0] + self.max_heap[0]) / 2
        else:
            return -self.min_heap[0]

# Example usage:
running_median = RunningMedian()
for num in [5, 3, 8, 4]:
    running_median.add_num(num)
    print(f"Current median: {running_median.get_median()}")