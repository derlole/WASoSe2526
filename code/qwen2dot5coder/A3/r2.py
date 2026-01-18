import asyncio

class EchoServerProtocol(asyncio.Protocol):
    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print(f'Connection from {peername}')
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print(f'Data received: {message}')
        
        # Echo the data back to the client
        self.transport.write(data)
        print('Data sent: {!r}'.format(message))

    def connection_lost(self, exc):
        peername = self.transport.get_extra_info('peername')
        if exc:
            print(f'Client {peername} closed with error {exc}')
        else:
            print(f'Client {peername} closed normally')

async def main():
    loop = asyncio.get_running_loop()
    server_coro = await loop.create_server(
        lambda: EchoServerProtocol(),
        '127.0.0.1', 8888)
    
    addr = server_coro.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server_coro:
        await server_coro.serve_forever()

asyncio.run(main())