import concurrent.futures
import time
from datetime import timedelta, datetime
import sched
import threading

# Define the deadline for the computation
deadline = datetime.now() + timedelta(seconds=10)  # Example: 10 seconds from now

def process_matrix_row(row):
    # Perform computation on the row
    time.sleep(0.1)  # Simulate computation time
    return sum(row)  # Example: Sum of elements in the row

def worker(task, lock, result):
    try:
        with lock:
            task()
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        with lock:
            result.append(1)  # Example: Increment a shared counter for the number of completed tasks

def main():
    num_cores = threading.active_count() - 2  # Subtract 2 for main and sched thread
    print(f"Number of CPU cores available: {num_cores}")

    lock = threading.Lock()
    result = []

    # Create a scheduler with a default delay of 0 seconds
    scheduler = sched.scheduler(time.time, time.sleep)

    def schedule_worker():
        if len(result) < num_cores:
            task = process_matrix_row
            worker_thread = threading.Thread(target=worker, args=(task, lock, result))
            worker_thread.start()
            scheduler.enter(0.1, 1, schedule_worker)

    # Start the computation with a specified deadline
    schedule_worker()
    scheduler.run(blocking=False)

    elapsed_time = (datetime.now() - deadline).total_seconds()
    print(f"Elapsed time: {elapsed_time} seconds")
    print(f"Number of completed tasks: {len(result)}")

if __name__ == "__main__":
    main()