import subprocess

def run_commands(command_list):
    # Initialize the first command
    proc = subprocess.Popen(command_list[0], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Pipe output to the next command in the list
    for cmd in command_list[1:]:
        proc = subprocess.Popen(cmd, shell=True, stdin=proc.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.stdout.read()  # Read the output to avoid blocking

    # Print the final output
    output, error = proc.communicate()

    if error:
        print("Error:", error.decode())
    else:
        print(output.decode())

if __name__ == "__main__":
    import sys

    # Get command-line arguments (commands)
    commands = sys.argv[1:]

    if not commands:
        print("Usage: python chain_cmds.py 'command1' 'command2' ... 'commandN'")
    else:
        run_commands(commands)