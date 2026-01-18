import subprocess

def run_command(command):
    """Run a shell command and return its stdout and stderr streams."""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return process

def stream_output(process):
    """Process the output of a command in real-time."""
    while True:
        # Read one line from stdout
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output, end='')

        # Read one line from stderr
        error = process.stderr.readline()
        if error == '' and process.poll() is not None:
            break
        if error:
            print(error, end='', file=sys.stderr)

def chain_commands(*commands):
    """Chain multiple commands and process their output in real time."""
    for command in commands:
        print(f"Running command: {command}")
        process = run_command(command)
        stream_output(process)
        process.wait()  # Wait for the command to finish before proceeding to the next one

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python chain_commands.py 'command1' 'command2' ... 'commandN'")
        sys.exit(1)

    # Get commands from command line arguments
    commands = sys.argv[1:]
    chain_commands(*commands)