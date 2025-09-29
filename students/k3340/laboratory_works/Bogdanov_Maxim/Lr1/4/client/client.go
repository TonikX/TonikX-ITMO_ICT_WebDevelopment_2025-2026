package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"strings"
)

// Клиент: первая строка - имя, затем пересылаем всё, что вводит пользователь.
// От сервера читаем в отдельной горутине, чтобы можно было одновременно печатать и получать.

func main() {
	serverAddr := "127.0.0.1:8080"
	if len(os.Args) > 1 {
		serverAddr = os.Args[1]
	}

	fmt.Print("Enter your name: ")
	in := bufio.NewReader(os.Stdin)
	name, _ := in.ReadString('\n')
	name = strings.TrimSpace(name)
	if name == "" {
		fmt.Println("Name cannot be empty")
		return
	}

	conn, err := net.Dial("tcp", serverAddr)
	if err != nil {
		fmt.Println("connect error:", err)
		return
	}
	defer conn.Close()

	// 1) Отправляем имя первой строкой
	fmt.Fprintln(conn, name)

	// 2) Горутина чтения из сервера
	go func() {
		r := bufio.NewScanner(conn)
		r.Buffer(make([]byte, 0, 1024), 64*1024)
		for r.Scan() {
			fmt.Println(r.Text())
		}
		os.Exit(0) // сервер закрыл соединение — выходим
	}()

	// 3) Главная петля: читаем stdin и шлём на сервер
	for {
		line, err := in.ReadString('\n')
		if err != nil {
			return
		}
		line = strings.TrimRight(line, "\r\n")
		if line == "" {
			continue
		}
		fmt.Fprintln(conn, line)
		if line == "/quit" {
			return
		}
	}
}
