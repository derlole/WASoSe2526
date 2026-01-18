import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging

class DirectoryWatcher(FileSystemEventHandler):
    def __init__(self, path_to_watch):
        self.path = path_to_watch

    def on_modified(self, event):
        if not event.is_directory:
            logging.info(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Modified: {event.src_path}")

    def on_created(self, event):
        if not event.is_directory:
            logging.info(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Created: {event.src_path}")

    def on_deleted(self, event):
        logging.info(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Deleted: {event.src_path}")

if __name__ == "__main__":
    path = "/path/to/your/directory"  # Replace with the path you want to monitor
    event_handler = DirectoryWatcher(path)

    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()