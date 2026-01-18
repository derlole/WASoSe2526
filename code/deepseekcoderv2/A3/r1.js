const net = require('net');
const async = require('async');

const PORT = 8080;
const ADDRESS = '0.0.0.0';
let connections = [];

const server = net.createServer((socket) => {
    console.log('Client connected');
    socket.on('data', (data) => {
        console.log(`Received data: ${data}`);
        // Echo back the received data to all clients
        connections.forEach(conn => {
            if (conn !== socket) conn.write(data);
        });
    });

    socket.on('close', () => {
        console.log('Client disconnected');
        const index = connections.indexOf(socket);
        if (index > -1) connections.splice(index, 1);
    });

    // Add new connection to the list
    connections.push(socket);
});

server.listen(PORT, ADDRESS, () => {
    console.log(`Server listening on ${ADDRESS}:${PORT}`);
});

// Handle concurrent connections using async library for demonstration purposes
const maxConnections = 1000;
let connectionQueue = [];
for (let i = 0; i < maxConnections; i++) {
    connectionQueue.push(function(callback) {
        server.listen(PORT, ADDRESS, () => {
            callback();
        });
    });
}

async.parallelLimit(connectionQueue, 100, (err, results) => {
    if (err) console.error(err);
    else console.log('All connections established');
});