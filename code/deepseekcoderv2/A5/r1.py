import subprocess
import sys
import os

def run_commands(commands):
    # Create a list to hold the processes
    processes = []
    
    for i, command in enumerate(commands):
        if i == 0:
            # Start the first process
            proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        else:
            # Start a new process with input from the previous process's output
            proc = subprocess.Popen(command, stdin=prev_proc.stdout, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        processes.append(proc)
        prev_proc = proc  # Update the reference to the previous process
    
    # Wait for all commands to complete and read their output in real time
    for proc in processes:
        while True:
            line = proc.stdout.readline()
            if not line:
                break
            sys.stdout.write(line.decode('utf-8'))
    
    # Wait for all subprocesses to complete
    for proc in processes:
        proc.wait()

if __name__ == "__main__":
    commands = [
        ["echo", "Hello, World!"],
        ["grep", "Hello"]
    ]
    
    run_commands(commands)