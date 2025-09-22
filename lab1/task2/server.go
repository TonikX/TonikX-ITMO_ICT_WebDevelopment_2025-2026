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

	jobs := make(chan job, 128)
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
