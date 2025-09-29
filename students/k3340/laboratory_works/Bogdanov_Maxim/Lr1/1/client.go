package main

import (
	"flag"
	"log"
	"net"
	"time"
)

const (
	defaultServerAddress = ":8080"
	defaultTimeout       = 3 * time.Second
)

func main() {
	server := flag.String("server", defaultServerAddress, "UDP server address host:port")
	timeout := flag.Duration("timeout", defaultTimeout, "read timeout")
	flag.Parse()

	raddr, err := net.ResolveUDPAddr("udp", *server)
	if err != nil {
		log.Fatalf("resolve server addr: %v", err)
	}

	conn, err := net.DialUDP("udp", nil, raddr)
	if err != nil {
		log.Fatalf("dial udp: %v", err)
	}
	defer func(conn *net.UDPConn) {
		err := conn.Close()
		if err != nil {
			log.Printf("close udp: %v", err)
		}
	}(conn)

	payload := []byte("Hello, server")
	if _, err := conn.Write(payload); err != nil {
		log.Fatalf("send: %v", err)
	}
	log.Printf("sent to %s: %q\n", raddr.String(), string(payload))

	if err := conn.SetReadDeadline(time.Now().Add(*timeout)); err != nil {
		log.Fatalf("set deadline: %v", err)
	}

	buf := make([]byte, 1024)
	n, err := conn.Read(buf)
	if err != nil {
		log.Fatalf("recv: %v", err)
	}
	log.Printf("from %s: %q", raddr.String(), string(buf[:n]))
}
