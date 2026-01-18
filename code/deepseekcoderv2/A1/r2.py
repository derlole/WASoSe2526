import heapq

class RunningMedianCalculator:
    def __init__(self):
        self.min_heap = []  # Stores the larger half of the data (in ascending order)
        self.max_heap = []  # Stores the smaller half of the data (in descending order)

    def add_number(self, num):
        if not self.min_heap or num > self.min_heap[0]:
            heapq.heappush(self.min_heap, num)
        else:
            heapq.heappush(self.max_heap, -num)
        
        # Balance the heaps so that the size of min_heap is equal to or one more than the size of max_heap
        if len(self.min_heap) > len(self.max_heap) + 1:
            heapq.heappush(self.max_heap, -heapq.heappop(self.min_heap))
        elif len(self.max_heap) > len(self.min_heap):
            heapq.heappush(self.min_heap, -heapq.heappop(self.max_heap))

    def get_median(self):
        if len(self.min_heap) == len(self.max_heap):
            return (self.min_heap[0] - self.max_heap[0]) / 2
        else:
            return self.min_heap[0]

# Example usage
if __name__ == "__main__":
    num_stream = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]  # Example stream of numbers
    running_median_calculator = RunningMedianCalculator()

    for num in num_stream:
        running_median_calculator.add_number(num)
        print("Added number:", num)
        print("Current median:", running_median_calculator.get_median())