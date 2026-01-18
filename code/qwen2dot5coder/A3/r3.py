import asyncio

class TCPServer:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port

    async def handle_client(self, reader, writer):
        try:
            while True:
                # Read data from the client
                data = await reader.read(1024)
                if not data:
                    break  # If no data received, close connection
                
                message = data.decode()
                print(f"Received: {message}")
                
                # Echo back the same data to the client
                writer.write(data)
                await writer.drain()
        except Exception as e:
            print(f"Error handling client: {e}")
        finally:
            print("Connection closed")
            writer.close()

    async def start_server(self):
        server = await asyncio.start_server(
            self.handle_client,
            self.host,
            self.port
        )
        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')

        async with server:
            await server.serve_forever()

def main():
    tcp_server = TCPServer()
    asyncio.run(tcp_server.start_server())

if __name__ == '__main__':
    main()