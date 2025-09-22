## Постановка задачи

Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python.

**Задание:**
- Сервер должен:
  - Принять и записать информацию о дисциплине и оценке по дисциплине.
  - Отдать информацию обо всех оценках по дисциплинам в виде HTML-страницы.

---

### client.go

```go
//go:build ignore
// +build ignore

package main

import (
	"encoding/json"
	"flag"
	"log"
	"net/url"
	"time"

	"github.com/gorilla/websocket"
)

var addr = flag.String("addr", "localhost:8080", "http service address")

type stat struct {
	Subject string `json:"subject"`
	Value   int    `json:"value"`
}

func main() {
	flag.Parse()

	u := url.URL{Scheme: "ws", Host: *addr, Path: "/stats/add"}
	c, _, err := websocket.DefaultDialer.Dial(u.String(), nil)
	if err != nil {
		log.Fatal("dial:", err)
	}
	defer c.Close()

	req := stat{Subject: "Math", Value: 5}
	data, _ := json.Marshal(req)
	if err := c.WriteMessage(websocket.TextMessage, data); err != nil {
		log.Fatal("write:", err)
	}

	c.SetReadDeadline(time.Now().Add(2 * time.Second))
	_, msg, err := c.ReadMessage()
	if err != nil {
		log.Println("no ack or error:", err)
	} else {
		log.Println("ack:", string(msg))
	}
	_ = c.Close()

	u = url.URL{Scheme: "ws", Host: *addr, Path: "/stats"}
	c2, _, err := websocket.DefaultDialer.Dial(u.String(), nil)
	if err != nil {
		log.Fatal("dial stats:", err)
	}
	defer c2.Close()

	_, p, err := c2.ReadMessage()
	if err != nil {
		log.Fatal("read stats:", err)
	}
	var arr []stat
	if err := json.Unmarshal(p, &arr); err != nil {
		log.Fatal("unmarshal stats:", err)
	}
	log.Printf("stats: %+v\n", arr)
}
```

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

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool { return true },
}

var (
	stats = make(map[string]int)
	mapMu sync.Mutex
)

type stat struct {
	Subject string `json:"subject"`
	Value   int    `json:"value"`
}

func main() {
	flag.Parse()
	http.HandleFunc("/stats", getStats)
	http.HandleFunc("/stats/add", addStat)
	log.Println("listening on", *addr)
	log.Fatal(http.ListenAndServe(*addr, nil))
}

func getStats(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println("upgrade:", err)
		return
	}
	defer conn.Close()

	mapMu.Lock()
	copySlice := make([]stat, 0, len(stats))
	for k, v := range stats {
		copySlice = append(copySlice, stat{Subject: k, Value: v})
	}
	mapMu.Unlock()

	b, err := json.Marshal(copySlice)
	if err != nil {
		_ = conn.WriteMessage(websocket.TextMessage, []byte("internal error"))
		return
	}

	if err := conn.WriteMessage(websocket.TextMessage, b); err != nil {
		log.Println("write:", err)
	}
}

func addStat(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Println("upgrade:", err)
		return
	}
	defer conn.Close()

	const numWorkers = 2
	jobs := make(chan []byte, 128)
	var wg sync.WaitGroup
	var writeMu sync.Mutex

	wg.Add(numWorkers)
	for i := 0; i < numWorkers; i++ {
		go func(id int) {
			defer wg.Done()
			for raw := range jobs {
				var req stat
				if err := json.Unmarshal(raw, &req); err != nil {
					writeMu.Lock()
					_ = conn.WriteMessage(websocket.TextMessage, []byte("invalid json: "+err.Error()))
					writeMu.Unlock()
					continue
				}
				if req.Subject == "" || req.Value <= 0 {
					writeMu.Lock()
					_ = conn.WriteMessage(websocket.TextMessage, []byte("invalid fields"))
					writeMu.Unlock()
					continue
				}

				mapMu.Lock()
				stats[req.Subject] = req.Value
				mapMu.Unlock()

				ack := []byte("ok:" + req.Subject + ":" + strconv.Itoa(req.Value))
				writeMu.Lock()
				_ = conn.WriteMessage(websocket.TextMessage, ack)
				writeMu.Unlock()
			}
		}(i)
	}

readLoop:
	for {
		_, raw, err := conn.ReadMessage()
		if err != nil {
			log.Println("read:", err)
			break readLoop
		}
		select {
		case jobs <- raw:
		default:
			writeMu.Lock()
			_ = conn.WriteMessage(websocket.TextMessage, []byte("server busy, drop"))
			writeMu.Unlock()
		}
	}

	close(jobs)
	wg.Wait()
	log.Println("addStat handler finished")
}
```

---

## Детали решения

- В примере используется WebSocket (пакет `github.com/gorilla/websocket`) для взаимодействия между клиентом и сервером по простому протоколу JSON.
- Сервер хранит оценки в `map[string]int` и защищает доступ мьютексом `mapMu`.
- Обработчик `addStat` принимает сообщения и обновляет структуру `stats`, а `getStats` возвращает текущий срез оценок в JSON или HTML (при желании можно сгенерировать страницу из этого JSON).

## Заключение

Пример показывает простой способ реализации сервера статистики/оценок. 

