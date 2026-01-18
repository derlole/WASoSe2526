import heapq
import struct

class RunningMedianCalculator:
    def __init__(self):
        self.lower_half = []  # Max heap to store lower half of numbers
        self.upper_half = []  # Min heap to store upper half of numbers
        self.total_count = 0

    def process(self, binary_stream):
        """Process a binary stream and compute the running median."""
        while True:
            data = binary_stream.recv(4)
            if not data:
                break

            num, = struct.unpack('>i', data)  # Unpack the integer value from the binary stream
            self.insert(num)

    def insert(self, num):
        """Insert a number into the heaps to maintain balance and update running median."""
        self.total_count += 1

        if not self.lower_half or num < -self.lower_half[0]:
            heapq.heappush(self.lower_half, -num)
        else:
            heapq.heappush(self.upper_half, num)

        # Rebalance heaps to ensure size difference is at most one
        if len(self.lower_half) > len(self.upper_half) + 1:
            heapq.heappush(self.upper_half, -heapq.heappop(self.lower_half))
        elif len(self.upper_half) > len(self.lower_half):
            heapq.heappush(self.lower_half, -heapq.heappop(self.upper_half))

        # Compute running median
        if self.total_count % 2 == 1:
            # Odd count: Median is the maximum value in lower half (or minimum value in upper half)
            return -self.lower_half[0]
        else:
            # Even count: Median is the average of max in lower half and min in upper half
            max_lower = -self.lower_half[0]
            min_upper = self.upper_half[0]

            return (max_lower + min_upper) / 2

# Example usage:
if __name__ == "__main__":
    import socket
    calculator = RunningMedianCalculator()

    # Create a TCP server to receive the binary stream
    host, port = 'localhost', 12345
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(1)

    print("Server listening on", (host, port))

    while True:
        connection, address = sock.accept()
        binary_stream = connection.makefile('rb')
        try:
            for i in range(10**8):
                median = calculator.process(binary_stream)
                if i % 1000000 == 0:
                    print(f"Median after {i} numbers: {median}")
        except KeyboardInterrupt:
            break
        finally:
            binary_stream.close()
            connection.close()
