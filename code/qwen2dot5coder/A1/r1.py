import heapq

class RunningMedian:
    def __init__(self):
        self.max_heap = []  # Max-heap for smaller numbers
        self.min_heap = []  # Min-heap for larger numbers

    def add_number(self, number):
        if len(self.max_heap) == 0 or number <= -self.max_heap[0]:
            heapq.heappush(self.max_heap, -number)
        else:
            heapq.heappush(self.min_heap, number)

        # Balance the heaps
        if len(self.max_heap) > len(self.min_heap) + 1:
            heapq.heappush(self.min_heap, -heapq.heappop(self.max_heap))
        elif len(self.min_heap) > len(self.max_heap):
            heapq.heappush(self.max_heap, -heapq.heappop(self.min_heap))

    def get_median(self):
        if len(self.max_heap) > len(self.min_heap):
            return -self.max_heap[0]
        else:
            return (-self.max_heap[0] + self.min_heap[0]) / 2.0

def process_stream(stream):
    running_median = RunningMedian()
    for number in stream:
        running_median.add_number(number)
        print(f"Current median: {running_median.get_median()}")

# Example usage with a simulated stream of numbers
if __name__ == "__main__":
    # Simulate a binary stream of integers
    import struct

    def read_int_from_stream(stream):
        return struct.unpack('i', stream.read(4))[0]

    # Assuming 'stream' is a file-like object opened in binary mode
    with open('numbers.bin', 'rb') as f:
        while True:
            data = f.read(4)  # Read 4 bytes for an integer
            if not data:
                break
            number = read_int_from_stream(f)
            process_stream([number])