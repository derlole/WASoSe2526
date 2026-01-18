#!/usr/bin/env python3
import asyncio
import sys

async def run_pipeline(commands):
    """
    Run a pipeline of commands asynchronously, piping their output to the next command.
    commands: List of commands, each as a list of strings, e.g. [['ls', '-l'], ['grep', 'py']]
    """
    processes = []
    prev_stdout = None

    for i, cmd in enumerate(commands):
        # Set stdin to previous process's stdout
        stdin = prev_stdout if prev_stdout else asyncio.subprocess.PIPE
        # Create the process
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=stdin,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        processes.append(proc)
        prev_stdout = proc.stdout  # pipe output to next process

    # Function to read and print output in real time
    async def stream_output(stream):
        while True:
            line = await stream.readline()
            if not line:
                break
            sys.stdout.buffer.write(line)
            await sys.stdout.flush()

    # Launch streaming tasks for the last process in the pipeline
    last_proc = processes[-1]
    await asyncio.gather(
        stream_output(last_proc.stdout),
        stream_output(last_proc.stderr)
    )

    # Wait for all processes to finish
    for proc in processes:
        await proc.wait()

def parse_commands():
    """
    Parse command line arguments into a list of commands.
    Example usage:
    ./pipeline.py "ls -l" "grep py" "sort"
    """
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <command1> [<command2> ...]")
        sys.exit(1)

    commands = [cmd.strip().split() for cmd in sys.argv[1:]]
    return commands

if __name__ == "__main__":
    cmds = parse_commands()
    asyncio.run(run_pipeline(cmds))
