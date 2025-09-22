//go:build ignore
// +build ignore

package main

import (
	"log"
	"net"
	"time"
)

func main() {
	conn, err := net.Dial("udp", "127.0.0.1:9000")
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()

	msg := []byte("hello, server!")
	conn.SetWriteDeadline(time.Now().Add(1 * time.Second))
	if _, err := conn.Write(msg); err != nil {
		log.Fatal("write:", err)
	}

	buf := make([]byte, 2048)
	conn.SetReadDeadline(time.Now().Add(2 * time.Second))
	n, err := conn.Read(buf)
	if err != nil {
		log.Println("read error:", err)
		return
	}
	log.Println("reply:", string(buf[:n]))
}
