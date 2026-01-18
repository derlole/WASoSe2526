import subprocess
from functools import partial
import sys

class CommandChain:
    def __init__(self):
        self.commands = []

    def add(self, cmd):
        """Add a command to the chain"""
        self.commands.append(cmd)

    def execute(self):
        """Execute all commands in sequence."""
        process = None
        for cmd in self.commands:
            if process is not None:
                # Close input stream of current process so new one can start consuming it.
                try:
                    process.stdin.close()
                except BrokenPipeError:
                    pass

            process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                       stdin=subprocess.PIPE)

            # Start reading output in the background
            self._read_process_output(process)

        # Wait for last process to finish and read any remaining output
        if process is not None:
            try:
                while True:
                    line = process.stdout.readline().decode('utf-8')
                    sys.stdout.write(line)
                    sys.stdout.flush()
            except BrokenPipeError:
                pass

    @staticmethod
    def _read_process_output(process):
        """Read and print output of a subprocess in real time."""
        while True:
            try:
                line = process.stdout.readline().decode('utf-8')
                if not line:
                    break
                sys.stdout.write(line)
                sys.stdout.flush()
            except (BrokenPipeError, EOFError):
                # Broken pipe means the parent finished consuming the output,
                # just stop reading
                return

    def __call__(self, *args, **kwargs):
        self.execute()


if __name__ == "__main__":
    chain = CommandChain()

    cmd1 = ["ls", "-l"]
    cmd2 = ["grep", "hello"]

    chain.add(cmd1)
    chain.add(cmd2)

    chain()