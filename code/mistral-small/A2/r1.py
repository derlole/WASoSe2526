import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
from datetime import datetime

class DirectoryChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        self.log_event("Modified", event)

    def on_created(self, event):
        self.log_event("Created", event)

    def on_deleted(self, event):
        self.log_event("Deleted", event)

    def log_event(self, action, event):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"{timestamp} - {action}: {event.src_path}"
        print(log_message)  # You can also write this to a file or send it via email, etc.

def monitor_directory(path_to_watch):
    event_handler = DirectoryChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=True)
    observer.start()

    print(f"Monitoring directory: {path_to_watch}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    path = "."  # Specify the directory you want to monitor here, e.g., "/path/to/directory"
    monitor_directory(path)