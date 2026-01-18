#!/usr/bin/env python3
"""
High-Throughput Asynchronous TCP Server
Handles 1,000+ concurrent connections using event-based I/O
"""

import asyncio
import signal
import sys
import time
from collections import defaultdict
from typing import Dict, Tuple

class HighThroughputTCPServer:
    """
    Asynchronous TCP server using asyncio for non-blocking I/O.
    Handles multiple concurrent connections efficiently without thread-per-connection.
    """
    
    def __init__(self, host: str = '0.0.0.0', port: int = 8888):
        self.host = host
        self.port = port
        self.server = None
        self.connections: Dict[Tuple[str, int], asyncio.StreamWriter] = {}
        self.stats = defaultdict(int)
        self.running = False
        
    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """
        Handle individual client connection asynchronously.
        
        Args:
            reader: AsyncIO stream reader for receiving data
            writer: AsyncIO stream writer for sending data
        """
        addr = writer.get_extra_info('peername')
        self.connections[addr] = writer
        self.stats['total_connections'] += 1
        self.stats['active_connections'] += 1
        
        print(f"[{time.strftime('%H:%M:%S')}] New connection from {addr[0]}:{addr[1]} "
              f"(Active: {self.stats['active_connections']})")
        
        try:
            while True:
                # Read data with timeout to detect idle connections
                try:
                    data = await asyncio.wait_for(reader.read(4096), timeout=300.0)
                except asyncio.TimeoutError:
                    print(f"[{time.strftime('%H:%M:%S')}] Timeout for {addr}")
                    break
                
                if not data:
                    # Client disconnected
                    break
                
                self.stats['messages_received'] += 1
                self.stats['bytes_received'] += len(data)
                
                # Process the request (minimal latency)
                start_time = time.perf_counter()
                response = await self.process_request(data)
                processing_time = (time.perf_counter() - start_time) * 1000
                
                # Send response back to client
                writer.write(response)
                await writer.drain()
                
                self.stats['messages_sent'] += 1
                self.stats['bytes_sent'] += len(response)
                
                # Track latency
                if processing_time > 10:  # Log slow requests (>10ms)
                    print(f"[{time.strftime('%H:%M:%S')}] Slow request from {addr}: {processing_time:.2f}ms")
                
        except asyncio.CancelledError:
            print(f"[{time.strftime('%H:%M:%S')}] Connection cancelled for {addr}")
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] Error handling {addr}: {e}")
        finally:
            # Cleanup
            self.stats['active_connections'] -= 1
            if addr in self.connections:
                del self.connections[addr]
            
            writer.close()
            await writer.wait_closed()
            print(f"[{time.strftime('%H:%M:%S')}] Connection closed for {addr[0]}:{addr[1]} "
                  f"(Active: {self.stats['active_connections']})")
    
    async def process_request(self, data: bytes) -> bytes:
        """
        Process incoming request data with minimal latency.
        This is where you implement your business logic.
        
        Args:
            data: Raw bytes received from client
            
        Returns:
            Response bytes to send back to client
        """
        # Example: Echo server with uppercase transformation
        # Replace this with your actual request processing logic
        
        try:
            message = data.decode('utf-8').strip()
            
            # Simulate minimal processing
            response = f"ECHO: {message.upper()}\n"
            
            return response.encode('utf-8')
        except Exception as e:
            return f"ERROR: {str(e)}\n".encode('utf-8')
    
    async def start(self):
        """Start the TCP server"""
        self.running = True
        
        # Create server with optimized settings
        self.server = await asyncio.start_server(
            self.handle_client,
            self.host,
            self.port,
            backlog=1024,  # Queue up to 1024 connections
            reuse_address=True,
            reuse_port=True  # Allow multiple processes to bind to same port
        )
        
        addr = self.server.sockets[0].getsockname()
        print(f"\n{'='*60}")
        print(f"High-Throughput TCP Server Started")
        print(f"{'='*60}")
        print(f"Listening on: {addr[0]}:{addr[1]}")
        print(f"Max connections: 1,000+")
        print(f"Mode: Asynchronous (event-based I/O)")
        print(f"{'='*60}\n")
        
        # Start statistics reporting
        asyncio.create_task(self.report_stats())
        
        async with self.server:
            await self.server.serve_forever()
    
    async def report_stats(self):
        """Periodically report server statistics"""
        while self.running:
            await asyncio.sleep(10)
            print(f"\n{'='*60}")
            print(f"Server Statistics - {time.strftime('%H:%M:%S')}")
            print(f"{'='*60}")
            print(f"Active connections: {self.stats['active_connections']}")
            print(f"Total connections: {self.stats['total_connections']}")
            print(f"Messages received: {self.stats['messages_received']}")
            print(f"Messages sent: {self.stats['messages_sent']}")
            print(f"Bytes received: {self.stats['bytes_received']:,}")
            print(f"Bytes sent: {self.stats['bytes_sent']:,}")
            print(f"{'='*60}\n")
    
    async def shutdown(self):
        """Gracefully shutdown the server"""
        print("\n\nShutting down server...")
        self.running = False
        
        # Close all active connections
        print(f"Closing {len(self.connections)} active connections...")
        for addr, writer in list(self.connections.items()):
            try:
                writer.close()
                await writer.wait_closed()
            except Exception as e:
                print(f"Error closing connection {addr}: {e}")
        
        # Stop the server
        if self.server:
            self.server.close()
            await self.server.wait_closed()
        
        print("Server stopped.")
        print(f"\nFinal Statistics:")
        print(f"Total connections served: {self.stats['total_connections']}")
        print(f"Total messages processed: {self.stats['messages_received']}")


async def main():
    """Main entry point"""
    # Configuration
    HOST = '0.0.0.0'  # Listen on all interfaces
    PORT = 8888       # Server port
    
    # Create server instance
    server = HighThroughputTCPServer(HOST, PORT)
    
    # Setup graceful shutdown
    loop = asyncio.get_running_loop()
    
    def signal_handler():
        print("\nReceived shutdown signal...")
        asyncio.create_task(server.shutdown())
        loop.stop()
    
    # Register signal handlers
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, signal_handler)
    
    try:
        await server.start()
    except KeyboardInterrupt:
        await server.shutdown()
    except Exception as e:
        print(f"Server error: {e}")
        await server.shutdown()


if __name__ == '__main__':
    # Set optimal event loop policy for performance
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped by user")