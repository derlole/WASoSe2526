import subprocess

def run_command(command):
    """Run a single command and return its process."""
    return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

def chain_commands(commands):
    """Chain multiple commands together and process their output in real-time."""
    processes = []

    # Start the first command
    first_process = run_command(commands[0])
    processes.append(first_process)
    current_process = first_process

    # Chain subsequent commands
    for cmd in commands[1:]:
        next_process = run_command(cmd)
        processes.append(next_process)

        # Pipe the output of the current process to the input of the next process
        while True:
            output = current_process.stdout.readline()
            if not output:
                break
            next_process.stdin.write(output)
        next_process.stdin.close()

        current_process = next_process

    # Capture and print the final output from the last command
    while True:
        output = current_process.stdout.readline()
        if not output:
            break
        print(output.decode().strip())

    for process in processes:
        process.wait()

def main():
    # Example commands to chain
    commands = [
        "echo 'Hello, world!'",
        "sed 's/world/Universe/'"
    ]

    chain_commands(commands)

if __name__ == "__main__":
    main()