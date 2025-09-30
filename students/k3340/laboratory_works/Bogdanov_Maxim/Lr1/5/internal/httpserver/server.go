package httpserver

import (
	"bufio"
	"fmt"
	"io"
	"net"
	"time"
)

type Config struct {
	Addr      string
	PublicDir string
}

const (
	maxRequestBytes = 64 * 1024
	readBufSize     = 4 * 1024
)

func ListenAndServe(cfg Config, r *Router) error {
	ln, err := net.Listen("tcp", cfg.Addr)
	if err != nil {
		return err
	}
	fmt.Printf("Server on http://%s\n", cfg.Addr)
	for {
		conn, err := ln.Accept()
		if err != nil {
			fmt.Println("accept:", err)
			continue
		}
		go handleConn(conn, r)
	}
}

func handleConn(c net.Conn, r *Router) {
	defer c.Close()

	limited := &io.LimitedReader{R: c, N: maxRequestBytes}
	br := bufio.NewReaderSize(limited, readBufSize)

	req, err := ReadRequest(br)
	if err != nil {
		WriteJSON(c, StatusBadRequest, H{"error": "Bad Request"})
		return
	}

	// читаем тело (если есть)
	if req.ContentLength > 0 {
		req.Body = make([]byte, req.ContentLength)
		if _, err := io.ReadFull(br, req.Body); err != nil {
			WriteJSON(c, StatusBadRequest, H{"error": "Bad Request Body"})
			return
		}
	}

	// роутинг
	if !r.Serve(c, req) {
		WriteText(c, StatusNotFound, "Not Found\n")
	}

	_ = c.SetDeadline(time.Now())
}
