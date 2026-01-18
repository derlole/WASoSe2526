import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define a class to handle file system events
class FileMonitorHandler(FileSystemEventHandler):
    def on_created(self, event):
        """Handle creation of new files"""
        print(f"File created: {event.src_path} at {event.event_type}")

    def on_deleted(self, event):
        """Handle deletion of existing files"""
        print(f"File deleted: {event.src_path} at {event.event_type}")

    def on_modified(self, event):
        """Handle modification of existing files"""
        print(f"File modified: {event.src_path} at {event.event_type}")


def main():
    # Specify the directory to monitor
    directory_to_monitor = '/path/to/your/directory'

    # Create an instance of the handler class
    handler = FileMonitorHandler()

    # Set up the event observer
    event_observer = Observer()
    event_observer.schedule(handler, directory_to_monitor, recursive=True)
    event_observer.start()

    try:
        # Run indefinitely until manually stopped
        while True:
            pass
    except KeyboardInterrupt:
        print("Event monitor stopped by user")
        event_observer.stop()
        event_observer.join()


if __name__ == "__main__":
    main()