package main

import (
	"log"
	"net"
	"os"
	"os/signal"
	"syscall"
)

const (
	address     = ":9000"
	readBufSize = 64 * 1024 // 64 KB
)

func main() {
	ln, err := net.Listen("tcp", address)
	if err != nil {
		log.Fatalf("listen error: %v", err)
	}
	defer ln.Close()

	log.Printf("High-throughput TCP server listening on %s", address)

	// Graceful shutdown handling
	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)

	go func() {
		<-sigCh
		log.Println("Shutting down server...")
		ln.Close()
		os.Exit(0)
	}()

	for {
		conn, err := ln.Accept()
		if err != nil {
			// Happens during shutdown
			continue
		}

		// Each connection is handled asynchronously
		go handleConnection(conn)
	}
}

func handleConnection(conn net.Conn) {
	defer conn.Close()

	buf := make([]byte, readBufSize)

	for {
		n, err := conn.Read(buf)
		if err != nil {
			return
		}

		// Immediate write-back (low latency)
		_, err = conn.Write(buf[:n])
		if err != nil {
			return
		}
	}
}
