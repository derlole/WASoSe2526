import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

class ChangeHandler(FileSystemEventHandler):
    def on_created(self, event):
        logging.info(f"File created: {event.src_path}")

    def on_deleted(self, event):
        logging.info(f"File deleted: {event.src_path}")

    def on_modified(self, event):
        logging.info(f"File modified: {event.src_path}")

def monitor_directory(path):
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    directory_to_monitor = "/path/to/directory"
    monitor_directory(directory_to_monitor)