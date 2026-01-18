#!/usr/bin/env python3
"""
High-Throughput TCP Server
Handles 1,000+ concurrent connections using asyncio event loop
"""

import asyncio
import time
import logging
from typing import Dict, Set
from dataclasses import dataclass
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class ConnectionStats:
    """Track connection statistics"""
    total_connections: int = 0
    active_connections: int = 0
    total_bytes_received: int = 0
    total_bytes_sent: int = 0
    total_requests: int = 0


class HighThroughputTCPServer:
    """
    Asynchronous TCP server with high concurrency support.
    Uses event-based I/O via asyncio for minimal latency.
    """
    
    def __init__(self, host: str = '0.0.0.0', port: int = 8888, backlog: int = 1024):
        self.host = host
        self.port = port
        self.backlog = backlog
        self.stats = ConnectionStats()
        self.active_tasks: Set[asyncio.Task] = set()
        self.client_registry: Dict[str, asyncio.StreamWriter] = {}
        
    async def handle_client(
        self, 
        reader: asyncio.StreamReader, 
        writer: asyncio.StreamWriter
    ) -> None:
        """
        Handle individual client connection asynchronously.
        
        Args:
            reader: Async stream reader for receiving data
            writer: Async stream writer for sending data
        """
        client_addr = writer.get_extra_info('peername')
        client_id = f"{client_addr[0]}:{client_addr[1]}"
        
        # Update statistics
        self.stats.total_connections += 1
        self.stats.active_connections += 1
        self.client_registry[client_id] = writer
        
        logger.info(f"New connection from {client_id} (Active: {self.stats.active_connections})")
        
        try:
            # Send welcome message
            welcome_msg = f"Connected to server. Your ID: {client_id}\n"
            writer.write(welcome_msg.encode())
            await writer.drain()
            self.stats.total_bytes_sent += len(welcome_msg)
            
            # Main client loop - handle requests
            while True:
                # Read data with timeout to prevent hanging
                try:
                    data = await asyncio.wait_for(
                        reader.read(4096),
                        timeout=300.0  # 5 minute timeout
                    )
                except asyncio.TimeoutError:
                    logger.warning(f"Client {client_id} timed out")
                    break
                
                if not data:
                    # Client disconnected
                    break
                
                # Update statistics
                self.stats.total_bytes_received += len(data)
                self.stats.total_requests += 1
                
                # Process request (echo server example with timestamp)
                request_start = time.perf_counter()
                
                # Decode and process
                message = data.decode('utf-8', errors='ignore').strip()
                
                # Handle special commands
                if message.lower() == 'quit' or message.lower() == 'exit':
                    response = "Goodbye!\n"
                    writer.write(response.encode())
                    await writer.drain()
                    break
                elif message.lower() == 'stats':
                    response = self._format_stats()
                elif message.lower() == 'ping':
                    response = "PONG\n"
                else:
                    # Echo back with timestamp
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                    response = f"[{timestamp}] Echo: {message}\n"
                
                # Send response
                writer.write(response.encode())
                await writer.drain()
                self.stats.total_bytes_sent += len(response)
                
                # Log latency
                request_time = (time.perf_counter() - request_start) * 1000
                if request_time > 10:  # Log if > 10ms
                    logger.warning(f"High latency: {request_time:.2f}ms for {client_id}")
                    
        except asyncio.CancelledError:
            logger.info(f"Handler for {client_id} cancelled")
        except Exception as e:
            logger.error(f"Error handling client {client_id}: {e}", exc_info=True)
        finally:
            # Cleanup
            self.stats.active_connections -= 1
            if client_id in self.client_registry:
                del self.client_registry[client_id]
            
            try:
                writer.close()
                await writer.wait_closed()
            except Exception as e:
                logger.error(f"Error closing connection for {client_id}: {e}")
            
            logger.info(f"Connection closed: {client_id} (Active: {self.stats.active_connections})")
    
    def _format_stats(self) -> str:
        """Format server statistics for display"""
        return (
            f"\n=== Server Statistics ===\n"
            f"Total Connections: {self.stats.total_connections}\n"
            f"Active Connections: {self.stats.active_connections}\n"
            f"Total Requests: {self.stats.total_requests}\n"
            f"Bytes Received: {self.stats.total_bytes_received:,}\n"
            f"Bytes Sent: {self.stats.total_bytes_sent:,}\n"
            f"========================\n"
        )
    
    async def start_server(self) -> None:
        """Start the TCP server"""
        server = await asyncio.start_server(
            self.handle_client,
            self.host,
            self.port,
            backlog=self.backlog,
            reuse_address=True,
            reuse_port=True  # Enable for load balancing across cores
        )
        
        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        logger.info(f"Server started on {addrs}")
        logger.info(f"Backlog: {self.backlog}, Ready for high-throughput connections")
        
        async with server:
            await server.serve_forever()
    
    async def stats_reporter(self, interval: int = 10) -> None:
        """Periodically report server statistics"""
        while True:
            await asyncio.sleep(interval)
            logger.info(
                f"Stats - Active: {self.stats.active_connections}, "
                f"Total: {self.stats.total_connections}, "
                f"Requests: {self.stats.total_requests}, "
                f"RX: {self.stats.total_bytes_received:,} bytes, "
                f"TX: {self.stats.total_bytes_sent:,} bytes"
            )
    
    async def run(self) -> None:
        """Run the server with stats reporting"""
        # Create tasks
        server_task = asyncio.create_task(self.start_server())
        stats_task = asyncio.create_task(self.stats_reporter())
        
        # Run until cancelled
        try:
            await asyncio.gather(server_task, stats_task)
        except KeyboardInterrupt:
            logger.info("Shutting down server...")
            server_task.cancel()
            stats_task.cancel()
            
            # Wait for tasks to complete
            await asyncio.gather(server_task, stats_task, return_exceptions=True)


def main():
    """Main entry point"""
    # Optimize event loop for high throughput
    if hasattr(asyncio, 'set_event_loop_policy'):
        # Use uvloop if available for better performance
        try:
            import uvloop
            asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
            logger.info("Using uvloop for enhanced performance")
        except ImportError:
            logger.info("Using default asyncio event loop")
    
    # Create and run server
    server = HighThroughputTCPServer(
        host='0.0.0.0',
        port=8888,
        backlog=2048  # Increased backlog for high concurrency
    )
    
    try:
        asyncio.run(server.run())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")


if __name__ == '__main__':
    main()