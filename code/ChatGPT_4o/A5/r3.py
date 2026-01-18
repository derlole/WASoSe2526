#!/usr/bin/env python3
import subprocess
import sys
from typing import List

def chain_commands(commands: List[List[str]]):
    """
    Chains multiple commands and processes their output in real-time.

    Args:
        commands: List of commands, where each command is a list of strings.
                  Example: [["ls", "-l"], ["grep", "py"], ["wc", "-l"]]
    """
    if not commands:
        print("No commands provided.")
        return

    processes = []
    prev_stdout = None

    for i, cmd in enumerate(commands):
        # For the first command, stdin is None; otherwise, it's the previous process's stdout
        stdin = prev_stdout
        # Create the subprocess with stdout as a pipe
        process = subprocess.Popen(
            cmd,
            stdin=stdin,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1  # Line-buffered for real-time streaming
        )
        # Close previous stdout in parent to allow proper SIGPIPE handling
        if prev_stdout:
            prev_stdout.close()
        prev_stdout = process.stdout
        processes.append(process)

    # Read from the last process in real-time
    try:
        assert prev_stdout is not None
        for line in prev_stdout:
            # Real-time processing: just print for now
            print(line, end='')
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
    finally:
        # Wait for all processes to finish
        for p in processes:
            p.wait()


def parse_args():
    """
    Parses command-line arguments into a list of command chains.
    Example usage:
        python3 pipe_tool.py "ls -l" "grep py" "wc -l"
    """
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} '<cmd1>' '<cmd2>' ...")
        sys.exit(1)

    commands = [arg.strip().split() for arg in sys.argv[1:]]
    return commands


if __name__ == "__main__":
    cmds = parse_args()
    chain_commands(cmds)
