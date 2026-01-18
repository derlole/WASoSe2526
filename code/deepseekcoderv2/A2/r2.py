import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class LogHandler(FileSystemEventHandler):
    def on_created(self, event):
        print(f'File created: {event.src_path} at {time.ctime(event.event_time)}')
    
    def on_deleted(self, event):
        print(f'File deleted: {event.src_path} at {time.ctime(event.event_time)}')
    
    def on_modified(self, event):
        print(f'File modified: {event.src_path} at {time.ctime(event.event_time)}')
    
    def on_moved(self, event):
        print(f'File moved from {event.src_path} to {event.dest_path} at {time.ctime(event.event_time)}')

if __name__ == "__main__":
    path = '/path/to/monitor'  # Specify the directory you want to monitor
    
    event_handler = LogHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    
    print(f"Monitoring {path}...")
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("Stopping monitoring.")
    
    observer.join()