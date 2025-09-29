package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net"
	"os"
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
	conn, err := net.Dial("tcp", "127.0.0.1:8080")
	if err != nil {
		panic(err)
	}
	defer func(conn net.Conn) {
		err := conn.Close()
		if err != nil {
			log.Printf("error closing connection: %v", err)
		}
	}(conn)

	fmt.Println("Выберите операцию:")
	fmt.Println("1 - Теорема Пифагора (a, b)")
	fmt.Println("2 - Решение квадратного уравнения ax^2 + bx + c = 0 (a, b, c)")
	fmt.Println("3 - Площадь трапеции (a, b, h)")
	fmt.Println("4 - Площадь параллелограмма (a, h)")

	var choice int
	if _, err := fmt.Scan(&choice); err != nil {
		fmt.Println("некорректный ввод:", err)
		return
	}

	var req Request
	switch choice {
	case 1:
		var a, b float64
		fmt.Print("Введите a и b: ")
		if _, err := fmt.Scan(&a, &b); err != nil {
			fmt.Println("некорректный ввод:", err)
			return
		}
		req = Request{Operation: "pythagoras", Params: []float64{a, b}}

	case 2:
		var a, b, c float64
		fmt.Print("Введите a, b, c: ")
		if _, err := fmt.Scan(&a, &b, &c); err != nil {
			fmt.Println("некорректный ввод:", err)
			return
		}
		req = Request{Operation: "quadratic", Params: []float64{a, b, c}}

	case 3:
		var a, b, h float64
		fmt.Print("Введите a, b, h: ")
		if _, err := fmt.Scan(&a, &b, &h); err != nil {
			fmt.Println("некорректный ввод:", err)
			return
		}
		req = Request{Operation: "trapezoid", Params: []float64{a, b, h}}

	case 4:
		var a, h float64
		fmt.Print("Введите a и h: ")
		if _, err := fmt.Scan(&a, &h); err != nil {
			fmt.Println("некорректный ввод:", err)
			return
		}
		req = Request{Operation: "parallelogram", Params: []float64{a, h}}

	default:
		fmt.Println("Неверный выбор.")
		os.Exit(1)
	}

	// Отправляем запрос и читаем ответ
	if err := json.NewEncoder(conn).Encode(req); err != nil {
		fmt.Println("ошибка отправки:", err)
		return
	}

	var resp Response
	if err := json.NewDecoder(conn).Decode(&resp); err != nil {
		fmt.Println("ошибка чтения ответа:", err)
		return
	}

	if resp.Error != "" {
		fmt.Println("Ошибка:", resp.Error)
	} else {
		fmt.Println("Результат:", resp.Result)
	}
}
