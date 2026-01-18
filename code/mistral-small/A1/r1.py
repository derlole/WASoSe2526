import sys
import heapq

class RunningMedian:
    def __init__(self):
        self.min_heap = []  # Max-heap by inverting values
        self.max_heap = []  # Min-heap

    def add_num(self, num):
        if not self.min_heap or num <= -self.min_heap[0]:
            heapq.heappush(self.min_heap, -num)
        else:
            heapq.heappush(self.max_heap, num)

        # Balance the heaps
        if len(self.min_heap) > len(self.max_heap) + 1:
            heapq.heappush(self.max_heap, -heapq.heappop(self.min_heap))
        elif len(self.max_heap) > len(self.min_heap):
            heapq.heappush(self.min_heap, -heapq.heppop(self.max_heap))

    def get_median(self):
        if len(self.min_heap) == len(self.max_heap):
            return (-self.min_heap[0] + self.max_heap[0]) / 2.0
        else:
            return -self.min_heap[0]

def process_stream(stream):
    running_median = RunningMedian()
    for num in stream:
        running_median.add_num(num)
        median = running_median.get_median()
        print(f"Running median after adding {num}: {median}")

if __name__ == "__main__":
    # Example usage
    input_stream = [7, 3, 5, 8, 6]
    process_stream(input_stream)