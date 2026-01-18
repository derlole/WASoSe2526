#!/usr/bin/env python3
"""
Command Pipeline Tool - Chain multiple system commands with real-time stream processing.

Usage:
    pipeline.py "command1 | command2 | command3"
    pipeline.py --file commands.txt
    
Examples:
    pipeline.py "cat /var/log/syslog | grep error | wc -l"
    pipeline.py "find . -name '*.py' | xargs wc -l | sort -rn"
"""

import sys
import subprocess
import shlex
import argparse
from typing import List, Optional
import signal


class CommandPipeline:
    """Manages execution of piped commands with real-time stream processing."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.processes: List[subprocess.Popen] = []
        
    def parse_pipeline(self, pipeline_str: str) -> List[str]:
        """Parse a pipeline string into individual commands."""
        # Split by pipe character while respecting quotes
        commands = []
        current_cmd = []
        in_quotes = False
        quote_char = None
        
        i = 0
        while i < len(pipeline_str):
            char = pipeline_str[i]
            
            if char in ('"', "'") and (i == 0 or pipeline_str[i-1] != '\\'):
                if not in_quotes:
                    in_quotes = True
                    quote_char = char
                elif char == quote_char:
                    in_quotes = False
                    quote_char = None
                current_cmd.append(char)
            elif char == '|' and not in_quotes:
                if current_cmd:
                    commands.append(''.join(current_cmd).strip())
                    current_cmd = []
            else:
                current_cmd.append(char)
            
            i += 1
        
        if current_cmd:
            commands.append(''.join(current_cmd).strip())
        
        return [cmd for cmd in commands if cmd]
    
    def execute_pipeline(self, commands: List[str], input_data: Optional[bytes] = None) -> int:
        """
        Execute a pipeline of commands with direct stream piping.
        
        Args:
            commands: List of command strings to execute
            input_data: Optional input data for the first command
            
        Returns:
            Exit code of the last command in the pipeline
        """
        if not commands:
            print("Error: No commands to execute", file=sys.stderr)
            return 1
        
        self.processes = []
        
        try:
            # Set up signal handling to propagate signals to child processes
            original_sigint = signal.signal(signal.SIGINT, self._signal_handler)
            original_sigterm = signal.signal(signal.SIGTERM, self._signal_handler)
            
            for i, cmd in enumerate(commands):
                if self.verbose:
                    print(f"[{i+1}/{len(commands)}] Executing: {cmd}", file=sys.stderr)
                
                # Determine stdin for this process
                if i == 0:
                    # First command: use provided input or inherit stdin
                    stdin = subprocess.PIPE if input_data is not None else sys.stdin
                else:
                    # Subsequent commands: pipe from previous process
                    stdin = self.processes[i-1].stdout
                
                # Determine stdout for this process
                if i == len(commands) - 1:
                    # Last command: write to stdout
                    stdout = sys.stdout
                else:
                    # Intermediate commands: pipe to next process
                    stdout = subprocess.PIPE
                
                # Create the process
                try:
                    process = subprocess.Popen(
                        shlex.split(cmd),
                        stdin=stdin,
                        stdout=stdout,
                        stderr=subprocess.PIPE,  # Capture stderr separately
                        bufsize=0  # Unbuffered for real-time processing
                    )
                    self.processes.append(process)
                    
                    # Allow previous process to receive SIGPIPE if next process exits
                    if i > 0 and self.processes[i-1].stdout is not None:
                        self.processes[i-1].stdout.close()
                    
                except FileNotFoundError:
                    print(f"Error: Command not found: {cmd.split()[0]}", file=sys.stderr)
                    self._cleanup_processes()
                    return 127
                except Exception as e:
                    print(f"Error starting command '{cmd}': {e}", file=sys.stderr)
                    self._cleanup_processes()
                    return 1
            
            # If we have input data, write it to the first process
            if input_data is not None and self.processes:
                try:
                    self.processes[0].communicate(input=input_data, timeout=None)
                except BrokenPipeError:
                    # First process may have exited early
                    pass
            
            # Wait for all processes and collect stderr
            return_code = 0
            for i, process in enumerate(self.processes):
                try:
                    _, stderr = process.communicate()
                    if stderr:
                        print(stderr.decode('utf-8', errors='replace'), 
                              file=sys.stderr, end='')
                    
                    if process.returncode != 0:
                        return_code = process.returncode
                        if self.verbose:
                            print(f"[{i+1}/{len(commands)}] Command exited with code {return_code}", 
                                  file=sys.stderr)
                except Exception as e:
                    print(f"Error waiting for process: {e}", file=sys.stderr)
                    return_code = 1
            
            # Restore signal handlers
            signal.signal(signal.SIGINT, original_sigint)
            signal.signal(signal.SIGTERM, original_sigterm)
            
            return return_code
            
        except KeyboardInterrupt:
            print("\nInterrupted by user", file=sys.stderr)
            self._cleanup_processes()
            return 130
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
            self._cleanup_processes()
            return 1
    
    def _signal_handler(self, signum, frame):
        """Handle signals by terminating all child processes."""
        self._cleanup_processes()
        sys.exit(128 + signum)
    
    def _cleanup_processes(self):
        """Terminate all running processes."""
        for process in reversed(self.processes):
            if process.poll() is None:  # Still running
                try:
                    process.terminate()
                    process.wait(timeout=1)
                except subprocess.TimeoutExpired:
                    process.kill()
                except Exception:
                    pass


def main():
    parser = argparse.ArgumentParser(
        description='Execute piped commands with real-time stream processing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "cat file.txt | grep error | wc -l"
  %(prog)s "ps aux | grep python | awk '{print $2}'"
  %(prog)s --verbose "find . -name '*.log' | xargs cat | grep ERROR"
  echo "data" | %(prog)s "tr a-z A-Z | rev"
        """
    )
    
    parser.add_argument(
        'pipeline',
        nargs='?',
        help='Pipeline of commands separated by | (e.g., "cmd1 | cmd2 | cmd3")'
    )
    parser.add_argument(
        '-f', '--file',
        help='Read pipeline commands from a file (one per line)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    parser.add_argument(
        '-i', '--input',
        help='Read input from a file instead of stdin'
    )
    
    args = parser.parse_args()
    
    # Determine the pipeline to execute
    if args.file:
        try:
            with open(args.file, 'r') as f:
                pipeline_str = ' | '.join(line.strip() for line in f if line.strip())
        except FileNotFoundError:
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            return 1
    elif args.pipeline:
        pipeline_str = args.pipeline
    else:
        parser.print_help()
        return 1
    
    # Prepare input data if specified
    input_data = None
    if args.input:
        try:
            with open(args.input, 'rb') as f:
                input_data = f.read()
        except Exception as e:
            print(f"Error reading input file: {e}", file=sys.stderr)
            return 1
    
    # Create and execute pipeline
    pipeline = CommandPipeline(verbose=args.verbose)
    commands = pipeline.parse_pipeline(pipeline_str)
    
    if not commands:
        print("Error: No valid commands found in pipeline", file=sys.stderr)
        return 1
    
    return pipeline.execute_pipeline(commands, input_data)


if __name__ == '__main__':
    sys.exit(main())