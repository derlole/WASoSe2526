import asyncio
from typing import Callable

class TcpServer:
    def __init__(self, host: str = 'localhost', port: int = 8080):
        self.host = host
        self.port = port
        self.server = None

    async def start(self):
        """Starts the TCP server."""
        self.server = await asyncio.start_server(
            self.handle_connection,
            self.host, self.port
        )

    async def stop(self):
        """Stops the TCP server."""
        if self.server:
            server = self.server
            self.server = None
            await server.close()

    async def handle_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Handles a single connection asynchronously."""
        data = await reader.read(100)
        message = data.decode()
        addr = writer.get_extra_info('peername')

        print(f"Received {message!r} from {addr!r}")

        # Send back the received message.
        writer.write(data)
        await writer.drain()

        # Make connection persistant
        reader.feed_eof = False

        # Close the connection
        print(f"Close the connection {addr!r}")
        writer.close()

    async def handle_request(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Handles a single request asynchronously."""
        data = await reader.read(100)
        message = data.decode()
        addr = writer.get_extra_info('peername')

        print(f"Received {message!r} from {addr!r}")

        # Send back the received message.
        writer.write(data)
        await writer.drain()

    async def run(self):
        """Runs the TCP server."""
        self.start()
        try:
            async with self.server:
                await self.server.serve_forever()
        except KeyboardInterrupt:
            print('Server stopped by user')
        finally:
            await self.stop()


# Usage
if __name__ == "__main__":
    asyncio.run(TcpServer().run())