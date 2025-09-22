//go:build ignore
// +build ignore

package main

import (
	_ "embed"
	"encoding/json"
	"flag"
	"log"
	"net/http"
	"strconv"
	"sync"

	"github.com/gorilla/websocket"
)

var addr = flag.String("addr", "localhost:8081", "http service address")

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool { return true },
}

var (
	stats = make(map[string][]int)
	mapMu sync.Mutex
)

//go:embed index.html
var indexHTML string

type statIn struct {
	Subject string `json:"subject"`
	Value   int    `json:"value"`
}

type statOut struct {
	Subject string `json:"subject"`
	Values  []int  `json:"values"`
}

func main() {
	flag.Parse()
	http.HandleFunc("/", serveIndex)
	http.HandleFunc("/stats", getStats)
	http.HandleFunc("/stats/add", addStat)
	log.Println("listening on", *addr)
	log.Fatal(http.ListenAndServe(*addr, nil))
}

func serveIndex(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	_, _ = w.Write([]byte(indexHTML))
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
	copySlice := make([]statOut, 0, len(stats))
	for k, v := range stats {
		vals := make([]int, len(v))
		copy(vals, v)
		copySlice = append(copySlice, statOut{Subject: k, Values: vals})
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
				var req statIn
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
				stats[req.Subject] = append(stats[req.Subject], req.Value)
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
