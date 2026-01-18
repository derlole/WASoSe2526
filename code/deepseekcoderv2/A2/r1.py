import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        logging.info(f'File created: {event.src_path}')

    def on_deleted(self, event):
        logging.info(f'File deleted: {event.src_path}')

    def on_modified(self, event):
        logging.info(f'File modified: {event.src_path}')

if __name__ == "__main__":
    path = 'your_directory_path'  # Replace with the directory you want to monitor
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)

    logging.info('Monitoring started...')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info('Monitoring stopped.')
    observer.join()