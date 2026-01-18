#!/usr/bin/env python3
"""
Streaming Median Calculator
Processes 10^8 integers from a binary stream and computes running median.
Uses dual-heap approach for O(log n) insertion and O(1) median retrieval.
"""

import heapq
import struct
import sys
import time
from typing import BinaryIO, Iterator


class StreamingMedian:
    """
    Efficiently computes running median using two heaps:
    - max_heap: stores smaller half of numbers (negated for max behavior)
    - min_heap: stores larger half of numbers
    
    Invariants:
    1. len(max_heap) == len(min_heap) or len(max_heap) == len(min_heap) + 1
    2. max(max_heap) <= min(min_heap)
    """
    
    def __init__(self):
        self.max_heap = []  # Lower half (negated values for max-heap behavior)
        self.min_heap = []  # Upper half
        self.count = 0
        
    def add_value(self, value: int) -> None:
        """Add a value and maintain heap invariants. O(log n) complexity."""
        self.count += 1
        
        # Add to max_heap first (negate for max-heap behavior)
        if not self.max_heap or value <= -self.max_heap[0]:
            heapq.heappush(self.max_heap, -value)
        else:
            heapq.heappush(self.min_heap, value)
        
        # Rebalance heaps
        if len(self.max_heap) > len(self.min_heap) + 1:
            heapq.heappush(self.min_heap, -heapq.heappop(self.max_heap))
        elif len(self.min_heap) > len(self.max_heap):
            heapq.heappush(self.max_heap, -heapq.heappop(self.min_heap))
    
    def get_median(self) -> float:
        """Get current median. O(1) complexity."""
        if not self.max_heap:
            raise ValueError("No values added yet")
        
        if len(self.max_heap) > len(self.min_heap):
            return float(-self.max_heap[0])
        else:
            return (-self.max_heap[0] + self.min_heap[0]) / 2.0


def read_binary_stream(stream: BinaryIO, num_values: int) -> Iterator[int]:
    """
    Read integers from binary stream (4 bytes per integer, little-endian).
    
    Args:
        stream: Binary input stream
        num_values: Number of integers to read
        
    Yields:
        Integer values from the stream
    """
    bytes_per_int = 4
    chunk_size = 65536  # Read in 64KB chunks for efficiency
    
    buffer = b''
    values_read = 0
    
    while values_read < num_values:
        chunk = stream.read(chunk_size)
        if not chunk:
            break
            
        buffer += chunk
        
        # Process complete integers from buffer
        while len(buffer) >= bytes_per_int and values_read < num_values:
            value = struct.unpack('<i', buffer[:bytes_per_int])[0]
            buffer = buffer[bytes_per_int:]
            yield value
            values_read += 1


def process_stream(input_stream: BinaryIO, num_values: int, 
                   report_interval: int = 10_000_000) -> StreamingMedian:
    """
    Process binary stream and compute running median.
    
    Args:
        input_stream: Binary input stream
        num_values: Total number of values to process
        report_interval: How often to report progress
        
    Returns:
        StreamingMedian object with final state
    """
    median_calc = StreamingMedian()
    start_time = time.time()
    
    print(f"Processing {num_values:,} values...")
    print(f"Progress updates every {report_interval:,} values\n")
    
    for i, value in enumerate(read_binary_stream(input_stream, num_values), 1):
        median_calc.add_value(value)
        
        # Report progress
        if i % report_interval == 0:
            elapsed = time.time() - start_time
            rate = i / elapsed
            median = median_calc.get_median()
            
            print(f"Processed: {i:>12,} values | "
                  f"Median: {median:>12.2f} | "
                  f"Rate: {rate:>10,.0f} values/sec | "
                  f"Elapsed: {elapsed:>6.1f}s")
    
    elapsed = time.time() - start_time
    final_rate = num_values / elapsed
    
    print(f"\n{'='*80}")
    print(f"Processing complete!")
    print(f"Total values: {num_values:,}")
    print(f"Total time: {elapsed:.2f} seconds")
    print(f"Average rate: {final_rate:,.0f} values/second")
    print(f"Final median: {median_calc.get_median():.2f}")
    print(f"{'='*80}\n")
    
    return median_calc


def generate_test_stream(filename: str, num_values: int, 
                        value_range: tuple = (-1_000_000, 1_000_000)) -> None:
    """
    Generate a binary test stream file.
    
    Args:
        filename: Output filename
        num_values: Number of values to generate
        value_range: (min, max) range for random values
    """
    import random
    
    print(f"Generating test stream: {filename}")
    print(f"Values: {num_values:,}, Range: {value_range}\n")
    
    with open(filename, 'wb') as f:
        chunk_size = 100_000
        for i in range(0, num_values, chunk_size):
            batch_size = min(chunk_size, num_values - i)
            values = [random.randint(*value_range) for _ in range(batch_size)]
            data = struct.pack(f'<{batch_size}i', *values)
            f.write(data)
            
            if (i + batch_size) % 10_000_000 == 0:
                print(f"Generated {i + batch_size:,} values...")
    
    print(f"Test stream generated successfully!\n")


def main():
    """Main entry point with example usage."""
    
    # Configuration
    NUM_VALUES = 100_000_000  # 10^8 values
    TEST_FILE = '/tmp/test_stream.bin'
    
    print("=" * 80)
    print("STREAMING MEDIAN CALCULATOR")
    print("=" * 80)
    print()
    
    # Option 1: Generate and process test data
    if len(sys.argv) == 1 or sys.argv[1] == '--test':
        print("Mode: Generate test data and process\n")
        generate_test_stream(TEST_FILE, NUM_VALUES)
        
        with open(TEST_FILE, 'rb') as f:
            result = process_stream(f, NUM_VALUES)
        
        print(f"Heap sizes: max_heap={len(result.max_heap):,}, "
              f"min_heap={len(result.min_heap):,}")
        
    # Option 2: Process from stdin
    elif sys.argv[1] == '--stdin':
        num_values = int(sys.argv[2]) if len(sys.argv) > 2 else NUM_VALUES
        print(f"Mode: Reading {num_values:,} values from stdin\n")
        result = process_stream(sys.stdin.buffer, num_values)
    
    # Option 3: Process from file
    elif sys.argv[1] == '--file':
        if len(sys.argv) < 3:
            print("Usage: python streaming_median.py --file <filename> [num_values]")
            sys.exit(1)
        
        filename = sys.argv[2]
        num_values = int(sys.argv[3]) if len(sys.argv) > 3 else NUM_VALUES
        print(f"Mode: Reading {num_values:,} values from {filename}\n")
        
        with open(filename, 'rb') as f:
            result = process_stream(f, num_values)
    
    else:
        print("Usage:")
        print("  python streaming_median.py [--test]              # Generate and process test data")
        print("  python streaming_median.py --stdin [num_values]  # Read from stdin")
        print("  python streaming_median.py --file <file> [num]   # Read from file")
        sys.exit(1)


if __name__ == '__main__':
    main()