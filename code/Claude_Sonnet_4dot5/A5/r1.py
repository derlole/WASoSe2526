#!/usr/bin/env python3
"""
PipeChain - A command-line tool for chaining multiple system commands with real-time stream processing.

Features:
- Direct stream piping (no temporary files)
- Real-time processing (output streams before previous commands finish)
- Efficient buffer management
- Proper process cleanup and error handling
"""

import sys
import subprocess
import argparse
import shlex
from typing import List, Optional, IO
import signal


class PipeChain:
    """Chains multiple system commands using direct stream piping."""
    
    def __init__(self, commands: List[str], verbose: bool = False, shell: bool = False):
        """
        Initialize the pipeline chain.
        
        Args:
            commands: List of command strings to chain
            verbose: Enable verbose logging to stderr
            shell: Execute commands through shell (allows shell features but less secure)
        """
        self.commands = commands
        self.verbose = verbose
        self.shell = shell
        self.processes: List[subprocess.Popen] = []
        
    def log(self, message: str):
        """Print log message to stderr if verbose mode is enabled."""
        if self.verbose:
            print(f"[PipeChain] {message}", file=sys.stderr, flush=True)
    
    def execute(self, stdin_input: Optional[str] = None) -> int:
        """
        Execute the command pipeline with real-time stream processing.
        
        Args:
            stdin_input: Optional input string to feed to first command
            
        Returns:
            Exit code of the last command in the chain
        """
        if not self.commands:
            print("Error: No commands provided", file=sys.stderr)
            return 1
        
        self.log(f"Executing pipeline with {len(self.commands)} command(s)")
        
        try:
            # Build the pipeline by starting all processes
            for i, cmd in enumerate(self.commands):
                self.log(f"Starting command {i+1}/{len(self.commands)}: {cmd}")
                
                # Determine input source for this process
                if i == 0:
                    # First command: use provided input or inherit stdin
                    if stdin_input is not None:
                        stdin = subprocess.PIPE
                    else:
                        stdin = None  # Inherit from parent process
                else:
                    # Subsequent commands: read from previous process's stdout
                    stdin = self.processes[i-1].stdout
                
                # Determine output destination for this process
                if i == len(self.commands) - 1:
                    # Last command: write to stdout
                    stdout = None  # Inherit from parent process
                else:
                    # Intermediate commands: pipe to next process
                    stdout = subprocess.PIPE
                
                # Parse command
                if self.shell:
                    cmd_args = cmd
                else:
                    cmd_args = shlex.split(cmd)
                
                # Start the subprocess
                process = subprocess.Popen(
                    cmd_args,
                    stdin=stdin,
                    stdout=stdout,
                    stderr=subprocess.PIPE,  # Capture stderr separately
                    shell=self.shell,
                    bufsize=0  # Unbuffered for real-time processing
                )
                
                self.processes.append(process)
                
                # Close stdout in parent to avoid deadlock
                # This allows the reading process to detect EOF
                if i > 0 and self.processes[i-1].stdout:
                    self.processes[i-1].stdout.close()
            
            # Feed input to first process if provided
            if stdin_input is not None and self.processes:
                self.log("Feeding input to first command")
                try:
                    self.processes[0].stdin.write(stdin_input.encode())
                    self.processes[0].stdin.close()
                except BrokenPipeError:
                    self.log("First command closed stdin early")
            
            # Collect stderr from all processes in real-time
            for i, process in enumerate(self.processes):
                if process.stderr:
                    # Read stderr without blocking
                    import threading
                    
                    def read_stderr(proc, cmd_num):
                        for line in proc.stderr:
                            sys.stderr.write(f"[cmd{cmd_num}] {line.decode()}")
                            sys.stderr.flush()
                    
                    stderr_thread = threading.Thread(
                        target=read_stderr,
                        args=(process, i+1),
                        daemon=True
                    )
                    stderr_thread.start()
            
            # Wait for all processes to complete
            exit_codes = []
            for i, process in enumerate(self.processes):
                returncode = process.wait()
                exit_codes.append(returncode)
                self.log(f"Command {i+1} finished with exit code {returncode}")
            
            # Return exit code of last command (standard Unix pipeline behavior)
            return exit_codes[-1] if exit_codes else 0
            
        except FileNotFoundError as e:
            print(f"Error: Command not found: {e}", file=sys.stderr)
            self.cleanup()
            return 127
        
        except KeyboardInterrupt:
            self.log("Interrupted by user")
            self.cleanup()
            return 130
        
        except Exception as e:
            print(f"Error executing pipeline: {e}", file=sys.stderr)
            self.cleanup()
            return 1
    
    def cleanup(self):
        """Terminate all running processes in the pipeline."""
        self.log("Cleaning up processes...")
        for i, process in enumerate(self.processes):
            if process.poll() is None:
                self.log(f"Terminating process {i+1}")
                process.terminate()
                try:
                    process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    self.log(f"Killing process {i+1}")
                    process.kill()
                    process.wait()


def main():
    """Main entry point for the PipeChain command-line tool."""
    
    parser = argparse.ArgumentParser(
        description="Chain multiple system commands with real-time stream processing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Basic piping:
    %(prog)s -c "echo hello world" -c "tr '[:lower:]' '[:upper:]'" -c "rev"
    
  Process log files:
    %(prog)s -c "cat /var/log/syslog" -c "grep ERROR" -c "tail -n 10"
    
  Real-time streaming:
    %(prog)s -c "tail -f logfile.txt" -c "grep pattern" -c "awk '{print $1}'"
    
  With stdin input:
    echo "data" | %(prog)s -c "sort" -c "uniq" -c "wc -l"
    
  Using input string:
    %(prog)s -i "line1\\nline2\\nline1" -c "sort" -c "uniq"
    
  Complex pipeline:
    %(prog)s -c "find . -name '*.py'" -c "xargs wc -l" -c "sort -rn" -c "head"

Note: Commands are executed with direct pipe connections for maximum efficiency.
No temporary files are created. Output streams in real-time.
        """
    )
    
    parser.add_argument(
        '-c', '--command',
        action='append',
        dest='commands',
        metavar='CMD',
        required=True,
        help='Command to add to the pipeline (specify multiple times for chaining)'
    )
    
    parser.add_argument(
        '-i', '--input',
        metavar='TEXT',
        help='Input text to feed to the first command'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging to stderr'
    )
    
    parser.add_argument(
        '-s', '--shell',
        action='store_true',
        help='Execute commands through shell (enables pipes, redirection, etc.)'
    )
    
    args = parser.parse_args()
    
    # Create and execute the pipeline
    pipeline = PipeChain(
        commands=args.commands,
        verbose=args.verbose,
        shell=args.shell
    )
    
    exit_code = pipeline.execute(stdin_input=args.input)
    sys.exit(exit_code)


if __name__ == '__main__':
    main()