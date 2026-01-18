import selectors
import socket
import threading

class TCPServer:
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        self.selector = selectors.DefaultSelector()
        self.server_socket = None
        self.connections = {}

    def start(self):
        # Create server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1024)  # Allow up to 1024 pending connections

        # Set up event loop
        self.selector.register(self.server_socket, selectors.EVENT_READ)

    def accept_connection(self):
        conn, addr = self.server_socket.accept()
        print(f'New connection from {addr}')

        # Register new connection with selector
        conn.setblocking(False)  # Allow non-blocking I/O
        self.selector.register(conn, selectors.EVENT_READ)
        self.connections[conn.fileno()] = conn

    def handle_request(self):
        while True:
            events = self.selector.select(timeout=None)

            for key, mask in events:
                if key.data is None:  # New connection
                    self.accept_connection()
                else:  # Existing connection
                    conn = key.data
                    try:
                        # Read incoming data from client
                        data = conn.recv(1024)
                        if not data:
                            print(f'Connection closed by {conn.getpeername()}')
                            self.selector.unregister(conn)
                            del self.connections[conn.fileno()]
                            continue

                        # Handle incoming request
                        # For simplicity, we just echo back the received message
                        response = f'Received: {data.decode()}'

                        # Send response to client
                        conn.sendall(response.encode())
                    except ConnectionResetError:
                        print(f'Connection reset by {conn.getpeername()}')
                        self.selector.unregister(conn)
                        del self.connections[conn.fileno()]

    def run(self):
        threading.Thread(target=self.handle_request).start()

        while True:
            # Keep server socket open for accepting new connections
            try:
                conn, addr = self.server_socket.accept()
                print(f'New connection from {addr}')
            except KeyboardInterrupt:
                break

if __name__ == '__main__':
    server = TCPServer()
    server.start()
    server.run()

    # Clean up on exit
    for conn in list(server.connections.values()):
        try:
            conn.close()
        except Exception as e:
            print(f'Error closing connection: {e}')