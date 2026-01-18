import subprocess
import sys

def run_command(command):
    """Run a single shell command and return its process."""
    return subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        stdin=subprocess.PIPE,
        text=True,
        bufsize=1,  # Line-buffered
        shell=True
    )

def chain_commands(commands):
    """Chain multiple commands and process their output in real time."""
    processes = []
    
    # Start the first command
    first_process = run_command(commands[0])
    processes.append(first_process)
    
    # Chain subsequent commands
    for command in commands[1:]:
        new_process = run_command(command)
        processes[-1].stdout.close()  # Close the previous process's stdout to free it up
        new_process.stdin = processes[-1].stdout  # Pipe output of previous process to input of current process
        processes.append(new_process)
    
    # Close the last command's stdin to end the pipeline
    processes[-1].stdin.close()
    
    return processes

def read_output(processes):
    """Read and print the combined output of all chained commands."""
    for line in processes[0].stdout:
        sys.stdout.write(line)
        sys.stdout.flush()

def main():
    if len(sys.argv) < 2:
        print("Usage: python chain_commands.py command1 | command2 | ...")
        sys.exit(1)
    
    # Parse the input commands
    commands = " ".join(sys.argv[1:]).split("|")
    commands = [command.strip() for command in commands]
    
    # Chain the commands and get the processes
    processes = chain_commands(commands)
    
    # Read and print the output of the first process
    read_output(processes)
    
    # Wait for all processes to finish
    for process in reversed(processes):
        process.wait()

if __name__ == "__main__":
    main()