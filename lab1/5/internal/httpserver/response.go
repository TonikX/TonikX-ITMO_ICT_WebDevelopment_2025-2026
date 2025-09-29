package httpserver

import (
	"encoding/json"
	"net"
	"strconv"
	"strings"
	"time"
)

const (
	StatusOK                  = "HTTP/1.1 200 OK"
	StatusCreated             = "HTTP/1.1 201 Created"
	StatusBadRequest          = "HTTP/1.1 400 Bad Request"
	StatusNotFound            = "HTTP/1.1 404 Not Found"
	StatusMethodNotAllowed    = "HTTP/1.1 405 Method Not Allowed"
	StatusUnsupportedMedia    = "HTTP/1.1 415 Unsupported Media Type"
	StatusInternalServerError = "HTTP/1.1 500 Internal Server Error"
)

type H map[string]any

func httpDate() string { return time.Now().UTC().Format("Mon, 02 Jan 2006 15:04:05 GMT") }

func writeResponse(c net.Conn, status string, headers map[string]string, body []byte) {
	if headers == nil {
		headers = map[string]string{}
	}
	if _, ok := headers["Content-Length"]; !ok {
		headers["Content-Length"] = strconv.Itoa(len(body))
	}
	if _, ok := headers["Date"]; !ok {
		headers["Date"] = httpDate()
	}
	if _, ok := headers["Connection"]; !ok {
		headers["Connection"] = "close"
	}
	if _, ok := headers["Server"]; !ok {
		headers["Server"] = "GoPureSocket/1.0"
	}

	var b strings.Builder
	b.WriteString(status + "\r\n")
	for k, v := range headers {
		b.WriteString(k + ": " + v + "\r\n")
	}
	b.WriteString("\r\n")
	c.Write([]byte(b.String()))
	if len(body) > 0 {
		c.Write(body)
	}
}

func WriteJSON(c net.Conn, status string, v any) {
	data, _ := json.Marshal(v)
	writeResponse(c, status, map[string]string{
		"Content-Type":  "application/json; charset=utf-8",
		"Cache-Control": "no-store",
	}, data)
}

func WriteText(c net.Conn, status string, s string) {
	writeResponse(c, status, map[string]string{
		"Content-Type": "text/plain; charset=utf-8",
	}, []byte(s))
}

func WriteBytes(c net.Conn, status string, contentType string, body []byte) {
	writeResponse(c, status, map[string]string{
		"Content-Type": contentType,
	}, body)
}
