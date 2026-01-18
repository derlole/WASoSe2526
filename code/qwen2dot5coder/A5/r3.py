import sys
import subprocess

def run_command(command):
    """Run a single command and yield its output line by line."""
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True  # This ensures that we receive the output as strings
    )

    for line in process.stdout:
        if process.poll() is None:
            yield line.strip()
        else:
            break

    return process.returncode, list(process.stderr)

def chain_commands(commands):
    """Chain multiple commands and process their output in real time."""
    previous_command = commands[0]
    for command in commands[1:]:
        # Run the previous command and capture its output
        for line in run_command(previous_command):
            print(line)
        
        # Use the output of the previous command as input to the next command
        previous_command = f"echo '{line}' | {command}"

    # Process the final command's output
    returncode, stderr = run_command(previous_command)
    if returncode != 0:
        print("An error occurred:", "\n".join(stderr), file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python chain_commands.py command1 | command2 | ...")
        sys.exit(1)

    # Parse the input commands
    commands = " ".join(sys.argv[1:]).split("|")

    # Chain and run the commands
    chain_commands(commands)