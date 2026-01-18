import subprocess

def chain_commands(command_chain):
    # Initialize the first command
    process = subprocess.Popen(command_chain[0], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # Process each subsequent command
    for cmd in command_chain[1:]:
        process = subprocess.Popen(cmd, shell=True, stdin=process.stdout, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        process.stdout.close()  # No need to read this as we'll read from the next command's stdout

    # Read and print output in real time
    while True:
        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
            break
        if output:
            print(output.strip().decode(), end='')

# Example usage
command_chain = [
    "ls -l",
    "grep '^d'",  # Filters lines starting with 'd' for directories
    "awk '{print $9}'"  # Extracts the last column (filename)
]

chain_commands(command_chain)