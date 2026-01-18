import heapq

class RunningMedianFinder:
    def __init__(self):
        self.min_heap = []  # Stores the larger half of numbers
        self.max_heap = []  # Stores the smaller half of numbers
    
    def add(self, num):
        if not self.max_heap or num <= -self.max_heap[0]:
            heapq.heappush(self.max_heap, -num)
        else:
            heapq.heappush(self.min_heap, num)
        
        # Balance the heaps to ensure they are within 1 element of each other in size
        if len(self.max_heap) > len(self.min_heap) + 1:
            heapq.heappush(self.min_heap, -heapq.heappop(self.max_heap))
        elif len(self.min_heap) > len(self.max_heap):
            heapq.heappush(self.max_heap, -heapq.heappop(self.min_heap))
    
    def find_median(self):
        if len(self.max_heap) == len(self.min_heap):
            return (-self.max_heap[0] + self.min_heap[0]) / 2
        else:
            return -self.max_heap[0]

# Example usage:
if __name__ == "__main__":
    rmf = RunningMedianFinder()
    
    # Simulate adding numbers from a stream (for demonstration purposes, we use a predefined list)
    data = [3, 1, 7, 5, 4, 2, 8, 6, 9, ...]  # This would be the continuous stream of integers
    
    for num in data:
        rmf.add(num)
        median = rmf.find_median()
        print("Current number:", num, "Median:", median)