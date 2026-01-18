#!/usr/bin/env python3
"""
File System Monitor
Monitors a directory for file system changes and logs them with timestamps.
Uses event-driven approach (no polling) via the watchdog library.
"""

import sys
import time
import logging
from datetime import datetime
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent


class FileChangeHandler(FileSystemEventHandler):
    """Handler for file system events with timestamp logging."""
    
    def __init__(self, log_file: str = None):
        """
        Initialize the handler.
        
        Args:
            log_file: Optional path to log file. If None, logs to console only.
        """
        super().__init__()
        self.setup_logging(log_file)
    
    def setup_logging(self, log_file: str = None):
        """Configure logging with timestamps."""
        # Create logger
        self.logger = logging.getLogger('FileSystemMonitor')
        self.logger.setLevel(logging.INFO)
        
        # Clear any existing handlers to avoid duplicates
        self.logger.handlers.clear()
        
        # Create formatter with timestamp
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler (if specified)
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def on_created(self, event: FileSystemEvent):
        """Called when a file or directory is created."""
        if not event.is_directory:
            self.logger.info(f"FILE CREATED: {event.src_path}")
        else:
            self.logger.info(f"DIRECTORY CREATED: {event.src_path}")
    
    def on_deleted(self, event: FileSystemEvent):
        """Called when a file or directory is deleted."""
        if not event.is_directory:
            self.logger.info(f"FILE DELETED: {event.src_path}")
        else:
            self.logger.info(f"DIRECTORY DELETED: {event.src_path}")
    
    def on_modified(self, event: FileSystemEvent):
        """Called when a file or directory is modified."""
        if not event.is_directory:
            self.logger.info(f"FILE MODIFIED: {event.src_path}")
        else:
            self.logger.info(f"DIRECTORY MODIFIED: {event.src_path}")
    
    def on_moved(self, event: FileSystemEvent):
        """Called when a file or directory is moved/renamed."""
        if not event.is_directory:
            self.logger.info(f"FILE MOVED: {event.src_path} -> {event.dest_path}")
        else:
            self.logger.info(f"DIRECTORY MOVED: {event.src_path} -> {event.dest_path}")


class FileSystemMonitor:
    """Main file system monitoring class."""
    
    def __init__(self, path: str, log_file: str = None, recursive: bool = True):
        """
        Initialize the file system monitor.
        
        Args:
            path: Directory path to monitor
            log_file: Optional path to log file
            recursive: Whether to monitor subdirectories recursively
        """
        self.path = Path(path).resolve()
        self.recursive = recursive
        self.event_handler = FileChangeHandler(log_file)
        self.observer = Observer()
        
        # Validate path
        if not self.path.exists():
            raise ValueError(f"Path does not exist: {self.path}")
        if not self.path.is_dir():
            raise ValueError(f"Path is not a directory: {self.path}")
    
    def start(self):
        """Start monitoring the file system."""
        print(f"\n{'='*70}")
        print(f"File System Monitor Started")
        print(f"{'='*70}")
        print(f"Monitoring: {self.path}")
        print(f"Recursive: {self.recursive}")
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}\n")
        print("Press Ctrl+C to stop monitoring...\n")
        
        # Schedule the observer
        self.observer.schedule(
            self.event_handler,
            str(self.path),
            recursive=self.recursive
        )
        
        # Start the observer
        self.observer.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop monitoring the file system."""
        print(f"\n{'='*70}")
        print("Stopping File System Monitor...")
        self.observer.stop()
        self.observer.join()
        print(f"Stopped at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}\n")


def main():
    """Main entry point for the file system monitor."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Monitor file system changes with timestamps',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Monitor current directory
  python file_monitor.py .
  
  # Monitor specific directory with log file
  python file_monitor.py /path/to/watch --log-file changes.log
  
  # Monitor without recursion
  python file_monitor.py /path/to/watch --no-recursive
        """
    )
    
    parser.add_argument(
        'path',
        help='Directory path to monitor'
    )
    
    parser.add_argument(
        '--log-file',
        help='Path to log file (optional, logs to console if not specified)'
    )
    
    parser.add_argument(
        '--no-recursive',
        action='store_true',
        help='Disable recursive monitoring of subdirectories'
    )
    
    args = parser.parse_args()
    
    try:
        monitor = FileSystemMonitor(
            path=args.path,
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