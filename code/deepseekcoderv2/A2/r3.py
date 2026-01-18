import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import logging

# Configure logging
log_dir = "./logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, 'file_changes.log'),
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        logging.info("File modified: {}".format(event.src_path))

    def on_created(self, event):
        logging.info("File created: {}".format(event.src_path))

    def on_deleted(self, event):
        logging.info("File deleted: {}".format(event.src_path))

if __name__ == "__main__":
    path = "./your_directory"  # Specify the directory to monitor
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()