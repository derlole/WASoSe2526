import asyncio

class HighThroughputTCPServer:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"Connection from {addr}")

        data = await reader.read(100)  # Read up to 100 bytes
        message = data.decode()

        print(f"Received {message} from {addr}")

        writer.write(data)  # Echo the received data back to the client
        await writer.drain()  # Wait for all data to be written

        print(f"Disconnected from {addr}")
        writer.close()
        await writer.wait_closed()

    async def start_server(self):
        server = await asyncio.start_server(self.handle_client, self.host, self.port)

        addr = server.sockets[0].getsockname()
        print(f"Serving on {addr}")

        async with server:
            await server.serve_forever()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    server = HighThroughputTCPServer()
    try:
        loop.run_until_complete(server.start_server())
    except KeyboardInterrupt:
        print("Stopping the server")
    finally:
        loop.close()