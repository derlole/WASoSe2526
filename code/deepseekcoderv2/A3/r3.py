import asyncio

# Maximum number of concurrent connections
MAX_CONNECTIONS = 1000

async def handle_connection(reader, writer):
    while True:
        data = await reader.readline()
        if not data:
            break
        message = data.decode().strip()
        print(f"Received: {message}")
        writer.write(data)  # Echo back the received message
        await writer.drain()
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_connection, '127.0.0.1', 8888)
    print("Server started on port 8888")

    async with server:
        # Set the maximum number of connections to MAX_CONNECTIONS
        tasks = asyncio.all_tasks()
        if len(tasks) < MAX_CONNECTIONS:
            await asyncio.create_task(server.serve_forever())
        else:
            print("Maximum number of concurrent connections reached.")

if __name__ == "__main__":
    asyncio.run(main())