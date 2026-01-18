import logging
from logging.handlers import RotatingFileHandler
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Set up logging configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    handlers=[RotatingFileHandler('file_system_monitor.log', maxBytes=10*1024*1024, backupCount=5)])

class FilesystemMonitor(FileSystemEventHandler):
    def on_created(self, event):
        """Log file creation events"""
        logging.info(f'File created: {event.src_path}')

    def on_deleted(self, event):
        """Log file deletion events"""
        logging.info(f'File deleted: {event.src_path}')

    def on_modified(self, event):
        """Log file modification events"""
        logging.info(f'File modified: {event.src_path}')

def monitor_directory(directory):
    """Start monitoring a directory for changes"""
    event_handler = FilesystemMonitor()
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()

    try:
        while True:
            # Keep the process alive (no need to implement polling here)
            pass
    except KeyboardInterrupt:
        observer.stop()
    finally:
        observer.join()

if __name__ == '__main__':
    directory = '/path/to/monitor'  # Replace with your target directory
    monitor_directory(directory)