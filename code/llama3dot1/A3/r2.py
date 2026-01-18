import socketserver
from select import select

class AsynchronousTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """Handle requests asynchronously using threads."""

    allow_reuse_address = True  # Set to true for the server to be able to restart quickly.
    daemon_threads = True       # To save resources and avoid zombie threads.

class RequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        """Process incoming data from a client."""
        try:
            # Receive data
            data = self.request.recv(1024)
            
            if not data:
                return

            # Process received data (e.g., send response back to the client)
            print(f"Received from {self.client_address[0]}: {data.decode()}")
            # Simulate latency in processing; you would replace this with your actual logic.
            import time
            time.sleep(0.01)  # Minimum non-zero latency for demonstration purposes.

            # Send response back to the client (this example just echoes what was received)
            self.request.sendall(data)

        except socket.error as e:
            print(f"Error on connection {self.client_address[0]}: {e}")

def main():
    with AsynchronousTCPServer(('localhost', 12345), RequestHandler) as server:
        # Start the server
        print("Server is running...")

        while True:
            try:
                # Main loop; allows the server to run indefinitely until interrupted manually.
                server.serve_forever()
            except KeyboardInterrupt:
                break

    print("Server stopped.")

if __name__ == "__main__":
    main()