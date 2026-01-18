import heapq
import struct
import sys

# Initialize two heaps: one max-heap (for lower half) and one min-heap (for upper half)
lower_half = []  # Max-heap to store the smaller half of the numbers
higher_half = []  # Min-heap to store the larger half of the numbers

def add_number(num):
    if not lower_half or num <= -lower_half[0]:
        heapq.heappush(lower_half, -num)
    else:
        heapq.heappush(higher_half, num)
    
    # Balance the heaps so that their sizes do not differ by more than 1
    if len(lower_half) > len(higher_half) + 1:
        heapq.heappush(higher_half, -heapq.heappop(lower_half))
    elif len(higher_half) > len(lower_half) + 1:
        heapq.heappush(lower_half, -heapq.heappop(higher_half))

def get_median():
    if len(lower_half) == len(higher_half):
        return (-lower_half[0] + higher_half[0]) / 2
    elif len(lower_half) > len(higher_half):
        return -lower_half[0]
    else:
        return higher_half[0]

def process_stream():
    # Assuming input is provided as a binary stream and read in chunks
    chunk_size = 1024 * 1024  # Read in chunks of 1 MB
    while True:
        data = sys.stdin.read(chunk_size)
        if not data:
            break
        nums = struct.unpack(f'{len(data) // 4}I', data)
        for num in nums:
            add_number(num)
            print("Median:", get_median())

if __name__ == "__main__":
    process_stream()