import subprocess
import sys
import threading

def run_command(cmd):
    """Run a command and handle its stdout and stderr."""
    process = subprocess.Popen(
        cmd,
        shell=True,  # Allow the use of shell for commands that require it
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True  # Use True to handle strings instead of bytes
    )
    return process

def read_stream(stream, prefix='', is_stderr=False):
    """Read and print the output from a stream in real time."""
    with stream:
        for line in iter(lambda: stream.readline(), b'' if is_stderr else ''):
            sys.stdout.write(f'{prefix}{line}')
            sys.stdout.flush()

def chain_commands(*cmds):
    """Chain multiple commands together, piping their outputs."""
    # Start the first command
    process = run_command(cmds[0])
    
    # Create threads to read stdout and stderr from each command
    thread1 = threading.Thread(target=read_stream, args=(process.stdout, cmds[0] + ' ',))
    thread2 = threading.Thread(target=read_stream, args=(process.stderr, cmds[0] + ' (err) ', True))
    
    # Start the threads
    thread1.start()
    thread2.start()
    
    # Wait for both threads to complete (they will run until the process finishes)
    thread1.join()
    thread2.join()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py '<command1> [<arg1>] [<arg2>:][<command2> [<arg1>:][<command3>...]'")
        sys.exit(1)
    
    # Split the command line arguments into separate commands
    cmds = ' '.join(sys.argv[1:]).split('|')
    
    # Chain all the commands together
    for i in range(len(cmds) - 1):
        chain_commands(cmds[i].strip(), cmds[i + 1].strip())