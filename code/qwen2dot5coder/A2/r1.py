import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            self.log_event('created', event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            self.log_event('deleted', event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.log_event('modified', event.src_path)

    @staticmethod
    def log_event(action, path):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"{timestamp} - {action}: {path}")

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
    directory_path = input("Enter the directory to monitor: ")
    monitor_directory(directory_path)