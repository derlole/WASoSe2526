import asyncio
from aiohttp import web

class HighThroughputTCPServer:
    def __init__(self, port):
        self.port = port
        self.app = web.Application()
        self.app.router.add_get('/', self.handle_request)

    async def handle_request(self, request):
        # Simulate a processing delay of 100 milliseconds
        await asyncio.sleep(0.1)
        return web.Response(text='Hello, client!')

    async def start_server(self):
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, 'localhost', self.port)
        await site.start()
        print(f'Server started on port {self.port}')
        while True:
            await asyncio.sleep(3600)  # Keep the server running indefinitely

if __name__ == '__main__':
    server = HighThroughputTCPServer(8080)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(server.start_server())
    loop.run_forever()