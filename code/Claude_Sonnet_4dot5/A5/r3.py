#!/usr/bin/env python3
"""
Command Pipeline Tool - Chains multiple system commands with real-time stream processing.

This tool allows you to chain multiple commands together, processing output in real-time
without waiting for previous commands to complete and without using temporary files.
"""

import subprocess
import sys
import argparse
import shlex
from typing import List, Optional
import signal


class CommandPipeline:
    """Manages a pipeline of chained system commands with real-time stream processing."""
    
    def __init__(self, commands: List[str], verbose: bool = False):
        """
        Initialize the command pipeline.
        
        Args:
            commands: List of command strings to chain together
            verbose: If True, print diagnostic information
        """
        self.commands = commands
        self.verbose = verbose
        self.processes: List[subprocess.Popen] = []
        
    def _log(self, message: str):
        """Print diagnostic message if verbose mode is enabled."""
        if self.verbose:
            print(f"[PIPELINE] {message}", file=sys.stderr)
    
    def execute(self, input_data: Optional[str] = None) -> int:
        """
        Execute the command pipeline with real-time stream processing.
        
        Args:
            input_data: Optional input to feed to the first command
            
        Returns:
            Exit code of the last command in the pipeline
        """
        if not self.commands:
            self._log("No commands to execute")
            return 0
        
        # Set up signal handler for clean shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        try:
            # Start all processes in the pipeline
            for i, cmd in enumerate(self.commands):
                self._log(f"Starting command {i + 1}/{len(self.commands)}: {cmd}")
                
                # Determine stdin for this process
                if i == 0:
                    # First command: use provided input or inherit stdin
                    stdin = subprocess.PIPE if input_data else sys.stdin
                else:
                    # Subsequent commands: use stdout of previous process
                    stdin = self.processes[i - 1].stdout
                
                # Determine stdout for this process
                if i == len(self.commands) - 1:
                    # Last command: output to stdout
                    stdout = sys.stdout
                else:
                    # Intermediate commands: pipe to next process
                    stdout = subprocess.PIPE
                
                # Start the process with unbuffered I/O for real-time processing
                process = subprocess.Popen(
                    shlex.split(cmd),
                    stdin=stdin,
                    stdout=stdout,
                    stderr=sys.stderr,
                    bufsize=0  # Unbuffered for real-time processing
                )
                
                self.processes.append(process)
                
                # Close stdout of previous process to allow SIGPIPE
                if i > 0:
                    self.processes[i - 1].stdout.close()
            
            # If input data was provided, write it to the first process
            if input_data and self.processes:
                self._log(f"Writing {len(input_data)} bytes to first command")
                try:
                    self.processes[0].stdin.write(input_data.encode())
                    self.processes[0].stdin.close()
                except BrokenPipeError:
                    self._log("First command terminated before consuming all input")
            
            # Wait for all processes to complete
            exit_codes = []
            for i, process in enumerate(self.processes):
                exit_code = process.wait()
                exit_codes.append(exit_code)
                self._log(f"Command {i + 1} exited with code {exit_code}")
            
            # Return the exit code of the last command
            return exit_codes[-1] if exit_codes else 0
            
        except Exception as e:
            self._log(f"Error executing pipeline: {e}")
            self._cleanup()
            raise
    
    def _signal_handler(self, signum, frame):
        """Handle interrupt signals by terminating all processes."""
        self._log(f"Received signal {signum}, terminating pipeline")
        self._cleanup()
        sys.exit(128 + signum)
    
    def _cleanup(self):
        """Terminate all running processes."""
        for i, process in enumerate(self.processes):
            if process.poll() is None:  # Process still running
                self._log(f"Terminating command {i + 1}")
                process.terminate()
                try:
                    process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    self._log(f"Force killing command {i + 1}")
                    process.kill()


def main():
    """Main entry point for the command pipeline tool."""
    parser = argparse.ArgumentParser(
        description="Chain multiple system commands with real-time stream processing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Chain multiple commands
  %(prog)s -c "seq 1 100" -c "grep 5" -c "wc -l"
  
  # Process data in real-time
  %(prog)s -c "cat largefile.txt" -c "grep pattern" -c "sort" -c "uniq -c"
  
  # Pipe input through commands
  echo "hello world" | %(prog)s -c "tr a-z A-Z" -c "rev"
  
  # Generate and filter data
  %(prog)s -c "seq 1 1000000" -c "grep 5" -c "head -20"
  
  # With verbose output
  %(prog)s -v -c "echo test" -c "cat" -c "wc -c"
        """
    )
    
    parser.add_argument(
        '-c', '--command',
        action='append',
        dest='commands',
        required=True,
        help='Command to execute (use multiple -c flags to chain commands)'
    )
    
    parser.add_argument(
        '-i', '--input',
        help='Input data to feed to the first command (if not using stdin)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output for debugging'
    )
    
    args = parser.parse_args()
    
    # Create and execute the pipeline
    pipeline = CommandPipeline(args.commands, verbose=args.verbose)
    exit_code = pipeline.execute(input_data=args.input)
    
    sys.exit(exit_code)


if __name__ == '__main__':
    main()