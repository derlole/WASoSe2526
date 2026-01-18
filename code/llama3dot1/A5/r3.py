import subprocess
from functools import partial
from typing import List, Callable, Any

class CommandChain:
    def __init__(self):
        self.commands = []
        self.pipes = []

    def add_command(self, cmd: str) -> 'CommandChain':
        """Add a new command to the chain"""
        self.commands.append(cmd)
        return self

    def start(self) -> None:
        """Start the chain and process output in real time"""
        self._start_piping()

    def _start_piping(self) -> None:
        if not self.commands:
            raise ValueError("No commands added to the chain")

        # Initialize pipes with the first command's stdout
        pipe = subprocess.Popen(self.commands[0], shell=True, 
                                stdin=subprocess.PIPE, 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE)

        self.pipes.append((pipe, None))

        for i in range(1, len(self.commands)):
            prev_pipe, _ = self.pipes[-1]
            cmd = self.commands[i]

            # Create a new subprocess and connect its stdin to the previous process's stdout
            pipe = subprocess.Popen(cmd, shell=True,
                                    stdin=prev_pipe.stdout, 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE)

            self.pipes.append((pipe, prev_pipe))

        # Start reading output from the last process in the chain
        _, _ = self._read_from_chain(self.pipes[-1][0])

    def _read_from_chain(self, pipe: subprocess.Popen) -> None:
        while True:
            try:
                line = pipe.stdout.readline().decode('utf-8')
                if not line:
                    break

                # For demonstration purposes, we'll just print the output
                # You can replace this with your own processing logic
                print(line.strip())
            except ValueError as e:
                # Handle invalid encoding
                print(f"Error reading from pipe: {e}")
                break

        # Wait for all processes to finish before cleaning up
        for _, prev_pipe in self.pipes[:-1]:
            _, _ = self._read_from_chain(prev_pipe)

    def run(self) -> None:
        """Run the command chain and process output"""
        try:
            self.start()
        except KeyboardInterrupt as e:
            print(f"Interrupted by user: {e}")
        finally:
            # Ensure all processes are killed
            for pipe, _ in self.pipes:
                pipe.kill()

# Example usage
if __name__ == "__main__":
    chain = CommandChain().add_command("ls -l").add_command("grep keyword")
    chain.start()