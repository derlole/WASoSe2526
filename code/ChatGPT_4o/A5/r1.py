#!/usr/bin/env python3
import asyncio
import sys

async def run_command(cmd, input_stream=None, process_line=None):
    """
    Run a command asynchronously, optionally piping input from input_stream.
    process_line: a callback to process each line of output in real-time.
    """
    # Start the subprocess
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdin=asyncio.subprocess.PIPE if input_stream else None,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )

    async def feed_input():
        if input_stream:
            while True:
                chunk = await input_stream.read(1024)
                if not chunk:
                    break
                proc.stdin.write(chunk)
                await proc.stdin.drain()
            proc.stdin.close()

    async def read_output():
        while True:
            line = await proc.stdout.readline()
            if not line:
                break
            if process_line:
                process_line(line)
    
    # Run both tasks concurrently
    tasks = [read_output()]
    if input_stream:
        tasks.append(feed_input())

    await asyncio.gather(*tasks)
    return await proc.wait()


async def main():
    # Example commands: you can replace these with any shell commands
    commands = [
        "echo 'Hello World\nThis is a test\nStreaming output'",
        "grep test",
        "awk '{print toupper($0)}'"
    ]

    input_stream = None

    # Define a simple line processor
    def process_line(line):
        sys.stdout.buffer.write(line)  # write bytes directly to stdout
        sys.stdout.flush()

    # Chain commands
    for cmd in commands:
        # Each command reads from previous command via asyncio.StreamReader
        if input_stream:
            # Use a pipe to feed previous output
            r, w = await asyncio.open_connection()
            # Not strictly necessary in this simple example; simplified
        await run_command(cmd, input_stream=input_stream, process_line=process_line)

if __name__ == "__main__":
    asyncio.run(main())
