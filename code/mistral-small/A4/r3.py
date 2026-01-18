import numpy as np
from multiprocessing import Pool, cpu_count, current_process
import time
import signal

# Signal handler to stop computation gracefully
def signal_handler(signum, frame):
    raise Exception("Deadline exceeded")

# Example matrix processing function
def process_matrix_chunk(chunk, result_dict):
    try:
        # Perform some computation on the chunk
        processed = np.sum(chunk)
        # Store the result in a shared dictionary
        result_dict[current_process().name] = processed
    except Exception as e:
        print(f"Error during processing: {e}")

# Main function to initiate parallel computation
def main():
    # Set the deadline (in seconds)
    deadline = 5

    # Signal handler for timeout
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(deadline)

    try:
        # Generate a large numerical matrix
        rows, cols = 10000, 10000
        matrix = np.random.rand(rows, cols)

        # Define the chunk size (number of rows per chunk)
        chunk_size = rows // cpu_count()

        # Initialize result dictionary
        results = {}

        # Create a pool of worker processes
        with Pool(processes=cpu_count()) as pool:
            # Split matrix into chunks and process in parallel
            for i in range(0, rows, chunk_size):
                chunk = matrix[i:i + chunk_size]
                pool.apply_async(process_matrix_chunk, (chunk, results))

        # Close the pool and wait for the work to finish
        pool.close()
        pool.join()

    except Exception as e:
        print(f"Exception occurred: {e}")

    finally:
        signal.alarm(0)  # Disable the alarm

    # Print results
    for key, value in results.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()