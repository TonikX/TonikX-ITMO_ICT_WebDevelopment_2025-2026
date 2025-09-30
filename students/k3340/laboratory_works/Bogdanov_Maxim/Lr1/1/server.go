package main

import (
	"context"
	"flag"
	"log"
	"net"
	"os"
	"os/signal"
	"syscall"
	"time"
)

const defaultUDPAddr = ":8080"

func main() {
	server := flag.String("server", defaultUDPAddr, "UDP server address host:port")
	flag.Parse()

	udpAddr, err := net.ResolveUDPAddr("udp", *server)
	if err != nil {
		log.Fatalf("resolve addr: %v", err)
	}

	conn, err := net.ListenUDP("udp", udpAddr)
	if err != nil {
		log.Fatalf("listen udp: %v", err)
	}
	defer func(conn *net.UDPConn) {
		err := conn.Close()
		if err != nil {
			log.Printf("close udp: %v", err)
		}
	}(conn)

	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer stop()

	go func() {
		for {
			select {
			case <-ctx.Done():
				return
			default:
			}
			_ = conn.SetReadDeadline(time.Now().Add(2 * time.Second))

			buf := make([]byte, 1024)

			n, clientAddr, err := conn.ReadFromUDP(buf)
			if ne, ok := err.(net.Error); ok && ne.Timeout() {
				continue
			}
			if err != nil {
				if ctx.Err() != nil {
					return
				}
				log.Printf("read error: %v", err)
				continue
			}

			msg := string(buf[:n])
			log.Printf("from %s: %q", clientAddr.String(), msg)

			reply := []byte("Hello, client")
			if _, err := conn.WriteToUDP(reply, clientAddr); err != nil {
				log.Printf("write error to %s: %v", clientAddr.String(), err)
			}
			log.Printf("sent to %s: %q\n", clientAddr.String(), string(reply))
		}
	}()

	<-ctx.Done()
	log.Println("shutting down…")
}
