import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            logging.info(f"File modified: {event.src_path}")

    def on_created(self, event):
        if not event.is_directory:
            logging.info(f"File created: {event.src_path}")

    def on_deleted(self, event):
        if not event.is_directory:
            logging.info(f"File deleted: {event.src_path}")

def monitor_directory(path_to_watch):
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    directory_path = "/path/to/directory"  # Replace with the directory you want to monitor
    monitor_directory(directory_path)