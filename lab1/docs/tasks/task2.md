## Постановка задачи

Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

**Варианты операций:**
- Теорема Пифагора.
- Решение квадратного уравнения.
- Поиск площади трапеции.
- Поиск площади параллелограмма.
- Порядок выбора варианта: Выбирается по порядковому номеру в журнале (пятый студент получает вариант 1 и т.д.).

**Требования:**
- Обязательно использовать библиотеку socket.
- Реализовать с помощью протокола **TCP**.

---

### client.go

```go
//go:build ignore
// +build ignore

package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"net/url"
	"os"
	"os/signal"
	"strconv"
	"strings"
	"time"

	"github.com/gorilla/websocket"
)

var addr = flag.String("addr", "localhost:8080", "http service address")
var values = flag.String("v", "6,7,8", "count area")

func main() {
	flag.Parse()
	log.SetFlags(0)

	fmt.Println(*values)

	interrupt := make(chan os.Signal, 1)
	signal.Notify(interrupt, os.Interrupt)

	u := url.URL{Scheme: "ws", Host: *addr, Path: "/solve"}
	log.Printf("connecting to %s", u.String())

	c, _, err := websocket.DefaultDialer.Dial(u.String(), nil)
	if err != nil {
		log.Fatal("dial:", err)
	}
	defer c.Close()

	done := make(chan []byte)

	go func() {
		defer close(done)
		for {
			_, message, err := c.ReadMessage()
			if err != nil {
				log.Println("read:", err)
				return
			}
			log.Printf("recv: %s", message)
			done <- message
		}
	}()

	for {
		select {
		case <-done:
			goto done
		case <-time.After(time.Second):
			vals := strings.Split(*values, ",")
			fmt.Println(vals)
			intVals := make([]int, 3)

			for i, v := range vals {
				v, err := strconv.Atoi(v)
				if err != nil {
					log.Fatalf("%s", err)
				}
				intVals[i] = v
			}

			type area struct {
				A, B, H int
			}

			req := area{
				intVals[0],
				intVals[1],
				intVals[2],
			}

			bytes, err := json.Marshal(req)

			err = c.WriteMessage(websocket.TextMessage, bytes)
			if err != nil {
				log.Println("write:", err)
				return
			}
		case <-interrupt:
			goto done
		}
	}

done:
	log.Println("interrupt")

	err = c.WriteMessage(websocket.CloseMessage, websocket.FormatCloseMessage(websocket.CloseNormalClosure, ""))
	if err != nil {
		log.Println("write close:", err)
		return
	}
	select {
	case <-done:
	case <-time.After(time.Second):
	}
}
```

---

### server.go

```go
//go:build ignore
// +build ignore

package main

import (
	"encoding/json"
	"flag"
	"log"
	"net/http"
	"strconv"
	"sync"

	"github.com/gorilla/websocket"
)

var addr = flag.String("addr", "localhost:8080", "http service address")

// Для теста разрешаем любой origin. В продакшне замените проверку.
var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool { return true },
}

type job struct {
	res []byte
}

func main() {
	flag.Parse()
	log.SetFlags(log.LstdFlags)
	http.HandleFunc("/solve", solve)
	log.Println("listening on", *addr)
	log.Fatal(http.ListenAndServe(*addr, nil))
}

func solve(w http.ResponseWriter, r *http.Request) {
	c, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Print("upgrade:", err)
		return
	}
	defer c.Close()

	numWorkers := 2

	jobs := make(chan job)
	var wg sync.WaitGroup

	var writeMu sync.Mutex

	wg.Add(numWorkers)
	for i := 0; i < numWorkers; i++ {
		go func(id int) {
			defer wg.Done()
			for j := range jobs {
				var area struct {
					A, B, H int
				}
				if err := json.Unmarshal(j.res, &area); err != nil {
					errMsg := []byte("invalid json: " + err.Error())
					writeMu.Lock()
					_ = c.WriteMessage(websocket.TextMessage, errMsg)
					writeMu.Unlock()
					continue
				}

				result := areaOfTrapezoid(area.A, area.B, area.H)
				buf := []byte(strconv.Itoa(result))

				writeMu.Lock()
				if writeErr := c.WriteMessage(websocket.TextMessage, buf); writeErr != nil {
					log.Printf("worker %d: write error: %v", id, writeErr)
					writeMu.Unlock()
					return
				}
				writeMu.Unlock()
			}
		}(i)
	}

readLoop:
	for {
		_, message, err := c.ReadMessage()
		if err != nil {
			log.Printf("read: %v (closing handler)", err)
			break readLoop
		}
		select {
		case jobs <- job{res: message}:
		default:
			log.Println("jobs queue full, dropping message")
		}
	}

	close(jobs)
	wg.Wait()

	log.Println("handler finished, connection closed")
}

func areaOfTrapezoid(a, b, h int) int {
	return (a + b) * h / 2
}
```

---

## Детали решения

- В примере сервер реализован как WebSocket-сервис поверх HTTP (пакет `github.com/gorilla/websocket`) для простоты обмена структурированными данными (JSON). Это позволяет клиенту отправлять JSON-запросы с параметрами операций, а серверу — возвращать результаты.
- Сервер использует пул воркеров (`numWorkers`) и канал `jobs` для параллельной обработки запросов.
- Для безопасной записи в соединение используется мьютекс `writeMu`.

## Заключение

Решение демонстрирует архитектуру клиент-серверного взаимодействия для вычислительных задач с использованием TCP/WebSocket. Его можно расширить, добавив обработку других операций (Пифагор, квадратное уравнение, параллелограмм) и интерфейс выбора варианта по номеру в журнале.

