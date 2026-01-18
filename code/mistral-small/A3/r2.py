import asyncio
from aiohttp import web

# Define the route handler for the server
async def handle_request(request):
    # Simulate some work with sleep
    await asyncio.sleep(0.1)  # Adjust based on your needs
    # Respond back to the client
    return web.Response(text="Hello, World!")

# Define the main function for starting the server
async def start_server():
    app = web.Application()
    app.router.add_get('/', handle_request)  # Add a GET route

    runner = web.AppRunner(app)
    await runner.setup()  # Setup the application

    site = web.TCPSite(runner, host='0.0.0.0', port=8080)  # Bind to all available IP addresses and port 8080
    await site.start()  # Start the server

# Run the event loop
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start_server())
        print("Server started at http://0.0.0.0:8080")
        # Keep the server running indefinitely
        loop.run_forever()
    except KeyboardInterrupt:
        pass  # Allow the server to gracefully shutdown
    finally:
        # Close the event loop
        loop.close()