// server.go
package main

import (
	"encoding/json"
	"fmt"
	"math"
	"net"
	"strings"
)

// Request - формат запроса клиент-сервер
type Request struct {
	Operation string    `json:"operation"`
	Params    []float64 `json:"params"`
}

// Response - формат ответа сервер-клиент
type Response struct {
	Result string `json:"result,omitempty"`
	Error  string `json:"error,omitempty"`
}

func main() {
	ln, err := net.Listen("tcp", ":8080")
	if err != nil {
		panic(err)
	}
	defer func(ln net.Listener) {
		err := ln.Close()
		if err != nil {
			fmt.Println(err)
		}
	}(ln)
	fmt.Println("TCP сервер запущен на :3000")

	for {
		conn, err := ln.Accept()
		if err != nil {
			fmt.Println("accept error:", err)
			continue
		}
		go handleConn(conn) // каждый клиент — в отдельной горутине
	}
}

func handleConn(c net.Conn) {
	defer func(c net.Conn) {
		err := c.Close()
		if err != nil {
			fmt.Println("close error:", err)
		}
	}(c)

	var req Request
	if err := json.NewDecoder(c).Decode(&req); err != nil {
		_ = json.NewEncoder(c).Encode(Response{Error: fmt.Sprintf("некорректный JSON: %v", err)})
		return
	}

	op := strings.ToLower(strings.TrimSpace(req.Operation))
	switch op {
	case "pythagoras":
		if len(req.Params) != 2 {
			writeErr(c, "ожидается 2 параметра: a, b")
			return
		}
		a, b := req.Params[0], req.Params[1]
		if a < 0 || b < 0 {
			writeErr(c, "a и b должны быть неотрицательны")
			return
		}
		res := math.Sqrt(a*a + b*b)
		writeOK(c, fmt.Sprintf("c = %.6f", res))

	case "quadratic":
		if len(req.Params) != 3 {
			writeErr(c, "ожидается 3 параметра: a, b, c")
			return
		}
		a, b, cc := req.Params[0], req.Params[1], req.Params[2]
		const eps = 1e-12
		if math.Abs(a) < eps {
			if math.Abs(b) < eps {
				if math.Abs(cc) < eps {
					writeOK(c, "бесконечно много решений (0 = 0)")
				} else {
					writeOK(c, "нет решений")
				}
				return
			}
			x := -cc / b
			writeOK(c, fmt.Sprintf("линейное уравнение: x = %.6f", x))
			return
		}
		D := b*b - 4*a*cc
		switch {
		case D > eps:
			sq := math.Sqrt(D)
			x1 := (-b - sq) / (2 * a)
			x2 := (-b + sq) / (2 * a)
			writeOK(c, fmt.Sprintf("D = %.6f > 0; x1 = %.6f, x2 = %.6f", D, x1, x2))
		case math.Abs(D) <= eps:
			x := -b / (2 * a)
			writeOK(c, fmt.Sprintf("D = 0; x = %.6f", x))
		default:
			absD := math.Sqrt(-D)
			re := -b / (2 * a)
			im := absD / (2 * a)
			writeOK(c, fmt.Sprintf("D = %.6f < 0; x1 = %.6f - %.6fi, x2 = %.6f + %.6fi", D, re, im, re, im))
		}

	case "trapezoid":
		if len(req.Params) != 3 {
			writeErr(c, "ожидается 3 параметра: a, b, h")
			return
		}
		a, b, h := req.Params[0], req.Params[1], req.Params[2]
		if a <= 0 || b <= 0 || h <= 0 {
			writeErr(c, "a, b, h должны быть > 0")
			return
		}
		S := (a + b) / 2 * h
		writeOK(c, fmt.Sprintf("S = %.6f", S))

	case "parallelogram":
		if len(req.Params) != 2 {
			writeErr(c, "ожидается 2 параметра: a, h")
			return
		}
		a, h := req.Params[0], req.Params[1]
		if a <= 0 || h <= 0 {
			writeErr(c, "a и h должны быть > 0")
			return
		}
		S := a * h
		writeOK(c, fmt.Sprintf("S = %.6f", S))

	default:
		writeErr(c, "неизвестная операция")
	}
}

func writeOK(c net.Conn, msg string) {
	_ = json.NewEncoder(c).Encode(Response{Result: msg})
}

func writeErr(c net.Conn, msg string) {
	_ = json.NewEncoder(c).Encode(Response{Error: msg})
}
