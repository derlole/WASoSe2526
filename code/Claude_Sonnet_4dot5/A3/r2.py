#!/usr/bin/env python3
"""
High-Throughput Asynchronous TCP Server
Handles 1,000+ concurrent connections using event-based non-blocking I/O
"""

import asyncio
import logging
import signal
import sys
from typing import Dict, Set
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class HighThroughputTCPServer:
    """
    Asynchronous TCP server using asyncio for high concurrency.
    Uses event loop with non-blocking I/O for minimal latency.
    """
    
    def __init__(self, host: str = '0.0.0.0', port: int = 8888):
        self.host = host
        self.port = port
        self.server = None
        self.active_connections: Set[asyncio.Task] = set()
        self.connection_count = 0
        self.stats = {
            'total_connections': 0,
            'total_messages': 0,
            'active_connections': 0,
            'start_time': None
        }
    
    async def handle_client(self, reader: asyncio.StreamReader, 
                          writer: asyncio.StreamWriter):
        """
        Handle individual client connection asynchronously.
        Each connection runs in the event loop without blocking.
        """
        addr = writer.get_extra_info('peername')
        self.connection_count += 1
        connection_id = self.connection_count
        self.stats['total_connections'] += 1
        self.stats['active_connections'] += 1
        
        logger.info(f"[Connection {connection_id}] New connection from {addr}")
        
        try:
            # Send welcome message
            welcome = f"Welcome to High-Throughput Server! Connection ID: {connection_id}\n"
            writer.write(welcome.encode())
            await writer.drain()
            
            # Main message loop
            while True:
                # Read data with timeout to detect dead connections
                try:
                    data = await asyncio.wait_for(reader.read(4096), timeout=300.0)
                except asyncio.TimeoutError:
                    logger.info(f"[Connection {connection_id}] Timeout - closing")
                    break
                
                if not data:
                    logger.info(f"[Connection {connection_id}] Client disconnected")
                    break
                
                # Process message
                message = data.decode('utf-8', errors='ignore').strip()
                self.stats['total_messages'] += 1
                
                # Handle different commands
                response = await self.process_message(connection_id, message)
                
                # Send response with minimal latency
                writer.write(response.encode())
                await writer.drain()
                
        except asyncio.CancelledError:
            logger.info(f"[Connection {connection_id}] Connection cancelled")
        except Exception as e:
            logger.error(f"[Connection {connection_id}] Error: {e}")
        finally:
            # Cleanup
            self.stats['active_connections'] -= 1
            logger.info(f"[Connection {connection_id}] Closing connection from {addr}")
            writer.close()
            await writer.wait_closed()
    
    async def process_message(self, connection_id: int, message: str) -> str:
        """
        Process incoming message and generate response.
        This is where you'd add your business logic.
        """
        message_lower = message.lower()
        
        if message_lower == 'stats':
            # Return server statistics
            uptime = datetime.now() - self.stats['start_time']
            return (
                f"\n=== Server Statistics ===\n"
                f"Active Connections: {self.stats['active_connections']}\n"
                f"Total Connections: {self.stats['total_connections']}\n"
                f"Total Messages: {self.stats['total_messages']}\n"
                f"Uptime: {uptime}\n"
                f"========================\n"
            )
        
        elif message_lower == 'ping':
            return "PONG\n"
        
        elif message_lower == 'time':
            return f"{datetime.now().isoformat()}\n"
        
        elif message_lower == 'help':
            return (
                "\n=== Available Commands ===\n"
                "STATS - Show server statistics\n"
                "PING  - Test connectivity\n"
                "TIME  - Get server time\n"
                "HELP  - Show this help\n"
                "QUIT  - Close connection\n"
                "==========================\n"
            )
        
        elif message_lower == 'quit':
            return "Goodbye!\n"
        
        else:
            # Echo the message back (default behavior)
            return f"[Echo] {message}\n"
    
    async def start(self):
        """
        Start the TCP server with optimized settings.
        """
        self.stats['start_time'] = datetime.now()
        
        # Create server with optimized parameters
        self.server = await asyncio.start_server(
            self.handle_client,
            self.host,
            self.port,
            backlog=1024,  # Accept queue size for high connection rates
            reuse_address=True,
            reuse_port=True  # Allow multiple processes to bind to same port
        )
        
        addr = self.server.sockets[0].getsockname()
        logger.info(f"Server started on {addr[0]}:{addr[1]}")
        logger.info(f"Ready to accept connections...")
        
        # Serve forever
        async with self.server:
            await self.server.serve_forever()
    
    async def shutdown(self):
        """
        Gracefully shutdown the server.
        """
        logger.info("Shutting down server...")
        
        if self.server:
            self.server.close()
            await self.server.wait_closed()
        
        # Cancel all active connections
        for task in self.active_connections:
            task.cancel()
        
        if self.active_connections:
            await asyncio.gather(*self.active_connections, return_exceptions=True)
        
        logger.info("Server shutdown complete")


async def main():
    """
    Main entry point with signal handling.
    """
    # Create server instance
    server = HighThroughputTCPServer(host='0.0.0.0', port=8888)
    
    # Setup signal handlers for graceful shutdown
    loop = asyncio.get_running_loop()
    
    def signal_handler():
        logger.info("Received shutdown signal")
        asyncio.create_task(server.shutdown())
        loop.stop()
    
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, signal_handler)
    
    try:
        await server.start()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received")
    finally:
        await server.shutdown()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped")
        sys.exit(0)