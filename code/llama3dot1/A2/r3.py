import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileChangeMonitor(FileSystemEventHandler):
    def __init__(self, path):
        self.path = path

    def on_created(self, event):
        print(f"{time.time()} - Created: {event.src_path}")

    def on_deleted(self, event):
        print(f"{time.time()} - Deleted: {event.src_path}")

    def on_modified(self, event):
        print(f"{time.time()} - Modified: {event.src_path}")

if __name__ == "__main__":
    path = "/path/to/monitor"  # Specify the directory you want to monitor
    monitor = FileChangeMonitor(path)
    observer = Observer()
    observer.schedule(monitor, path, recursive=True)  
    observer.start()

    try:
        while True:
            time.sleep(1)  # Sleep for 1 second before checking again
    except KeyboardInterrupt:
        observer.stop()
        observer.join()