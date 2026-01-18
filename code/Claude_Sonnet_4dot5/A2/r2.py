#!/usr/bin/env python3
"""
File System Monitor - Event-driven file system change tracking
Uses watchdog library for immediate, non-polling file system monitoring
"""

import sys
import time
from datetime import datetime
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent


class FileChangeLogger(FileSystemEventHandler):
    """Handler that logs all file system events with timestamps"""
    
    def __init__(self, log_file=None):
        super().__init__()
        self.log_file = log_file
        
    def _log_event(self, event_type: str, path: str, is_directory: bool = False):
        """Log an event with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        item_type = "directory" if is_directory else "file"
        message = f"[{timestamp}] {event_type}: {item_type} '{path}'"
        
        print(message)
        
        if self.log_file:
            with open(self.log_file, 'a') as f:
                f.write(message + '\n')
    
    def on_created(self, event: FileSystemEvent):
        """Called when a file or directory is created"""
        self._log_event("CREATED", event.src_path, event.is_directory)
    
    def on_deleted(self, event: FileSystemEvent):
        """Called when a file or directory is deleted"""
        self._log_event("DELETED", event.src_path, event.is_directory)
    
    def on_modified(self, event: FileSystemEvent):
        """Called when a file or directory is modified"""
        # Skip directory modification events as they can be noisy
        if not event.is_directory:
            self._log_event("MODIFIED", event.src_path, event.is_directory)
    
    def on_moved(self, event: FileSystemEvent):
        """Called when a file or directory is moved or renamed"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        item_type = "directory" if event.is_directory else "file"
        message = f"[{timestamp}] MOVED: {item_type} from '{event.src_path}' to '{event.dest_path}'"
        
        print(message)
        
        if self.log_file:
            with open(self.log_file, 'a') as f:
                f.write(message + '\n')


class FileSystemMonitor:
    """Main monitor class that sets up and manages the file system observer"""
    
    def __init__(self, watch_path: str, log_file: str = None, recursive: bool = True):
        """
        Initialize the file system monitor
        
        Args:
            watch_path: Directory path to monitor
            log_file: Optional file path to write logs to
            recursive: Whether to monitor subdirectories
        """
        self.watch_path = Path(watch_path).resolve()
        self.log_file = log_file
        self.recursive = recursive
        self.observer = None
        
        # Validate watch path
        if not self.watch_path.exists():
            raise ValueError(f"Watch path does not exist: {self.watch_path}")
        if not self.watch_path.is_dir():
            raise ValueError(f"Watch path is not a directory: {self.watch_path}")
    
    def start(self):
        """Start monitoring the file system"""
        print(f"Starting file system monitor...")
        print(f"Watching: {self.watch_path}")
        print(f"Recursive: {self.recursive}")
        if self.log_file:
            print(f"Logging to: {self.log_file}")
        print(f"Press Ctrl+C to stop\n")
        
        # Create event handler and observer
        event_handler = FileChangeLogger(log_file=self.log_file)
        self.observer = Observer()
        self.observer.schedule(event_handler, str(self.watch_path), recursive=self.recursive)
        
        # Start the observer
        self.observer.start()
        
        try:
            # Keep the main thread alive
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop monitoring the file system"""
        if self.observer:
            print("\n\nStopping file system monitor...")
            self.observer.stop()
            self.observer.join()
            print("Monitor stopped.")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Monitor file system changes and log them with timestamps',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Monitor current directory
  python file_monitor.py .
  
  # Monitor specific directory with log file
  python file_monitor.py /path/to/watch --log changes.log
  
  # Monitor without recursion
  python file_monitor.py /path/to/watch --no-recursive
        """
    )
    
    parser.add_argument(
        'path',
        help='Directory path to monitor'
    )
    parser.add_argument(
        '--log',
        '-l',
        dest='log_file',
        help='Optional log file to write events to'
    )
    parser.add_argument(
        '--no-recursive',
        action='store_true',
        help='Do not monitor subdirectories'
    )
    
    args = parser.parse_args()
    
    try:
        monitor = FileSystemMonitor(
            watch_path=args.path,
            log_file=args.log_file,
            recursive=not args.no_recursive
        )
        monitor.start()
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
