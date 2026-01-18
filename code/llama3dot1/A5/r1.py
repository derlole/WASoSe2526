import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

def chain_commands(commands):
    """
    Chain multiple system commands and process their output in real time.
    
    Args:
        commands (list): A list of tuples where each tuple contains a command to execute,
                         the type of stdin data it expects, and how it should handle
                         its stdout. The format is (command, [stdin_type], [stdout_handler]).
        
    Returns:
        None
    """
    with ThreadPoolExecutor(max_workers=len(commands)) as executor:
        futures = []
        
        # Create a process for each command in the list
        for command in commands:
            cmd, stdin_type, stdout_handler = command
            
            if stdin_type == 'pipe':
                # If this is the first command, redirect stdout to pipe
                if not futures:
                    with open('/dev/null', 'w') as dev_null:
                        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=dev_null)
                else:
                    # Otherwise, pipe output from previous command to current one
                    prev_process = futures[-1].process
                    process = subprocess.Popen(cmd, shell=True, stdin=prev_process.stdout, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                
                future = executor.submit(process_stdout, process, stdout_handler)
            else:
                # If the command doesn't expect any input, just run it and attach to its output stream
                process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                future = executor.submit(process_stdout, process, stdout_handler)
            
            futures.append(future)
        
        # Process stdout from each command as it becomes available
        for future in as_completed(futures):
            future.result()

def process_stdout(process, handler):
    """
    Process the output of a subprocess.
    
    Args:
        process: The subprocess object that generated the output.
        handler (function): A function to handle the output. It should take one argument,
                            which is the line from stdout.
        
    Returns:
        None
    """
    for line in iter(process.stdout.readline, b''):
        line = line.decode('utf-8').rstrip()
        handler(line)
    
    # Close the process's stdout stream so it terminates
    process.stdout.close()

# Example usage:

commands = [
    ('ls -l', 'none', print),
    ('grep keyword', 'pipe', lambda x: print(f'Keyword found on line {x}')),
    ('sort', 'pipe', lambda x: print(f'Sorted line: {x}'))
]

chain_commands(commands)