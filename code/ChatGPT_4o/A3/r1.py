import asyncio

async def tcp_client(message: str):
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)
    writer.write(message.encode())
    await writer.drain()
    data = await reader.read(1024)
    print(f"Received: {data.decode()}")
    writer.close()
    await writer.wait_closed()

async def main():
    tasks = [tcp_client(f"Hello {i}") for i in range(1000)]
    await asyncio.gather(*tasks)

asyncio.run(main())
