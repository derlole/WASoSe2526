import subprocess
import sys
import threading

def run_command(cmd):
    """Run a command and handle its output."""
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        text=True  # Use True to treat the output as strings
    )

    def forward_output():
        """Forward the output of the subprocess to the standard output."""
        for line in iter(lambda: process.stdout.read(1), b''):
            sys.stdout.write(line)
            sys.stdout.flush()

    # Start a thread to read and print stdout
    threading.Thread(target=forward_output, daemon=True).start()

    # Read and handle stderr if needed
    for line in iter(lambda: process.stderr.read(1), b''):
        sys.stderr.write(line)
        sys.stderr.flush()

    # Wait for the command to complete
    process.wait()

def main():
    """Main function to run commands chain."""
    if len(sys.argv) < 2:
        print("Usage: python script.py <command1> [<arg1> ...] [-- <command2> [<arg2> ...]]")
        sys.exit(1)

    # Extract the command and its arguments
    cmd_args = sys.argv[1:]
    delimiter_index = cmd_args.index('--') if '--' in cmd_args else len(cmd_args)

    # Split commands
    first_command = cmd_args[:delimiter_index]
    subsequent_commands = cmd_args[delimiter_index + 1:]

    # Run the first command
    run_command(first_command)

    # Optionally run subsequent commands if they are provided
    for sub_cmd in subsequent_commands:
        run_command([sub_cmd])

if __name__ == "__main__":
    main()