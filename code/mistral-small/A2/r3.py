import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging

# Setup logging configuration to include timestamps
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        logging.info(f'Modified: {event.src_path}')

    def on_created(self, event):
        logging.info(f'Created: {event.src_path}')

    def on_deleted(self, event):
        logging.info(f'Deleted: {event.src_path}')

def monitor_directory(path_to_watch):
    event_handler = ChangeHandler()
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
    path = "./"  # Change this to the directory you want to monitor
    monitor_directory(path)