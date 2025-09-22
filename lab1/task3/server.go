package main

import (
	"flag"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/gorilla/websocket"
)

var addr = flag.String("addr", "localhost:8080", "http service address")

var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool { return true },
}

var indexHTML []byte

func main() {
	flag.Parse()

	var err error
	indexHTML, err = os.ReadFile("index.html")
	if err != nil {
		log.Fatalf("read index.html: %v", err)
	}

	http.HandleFunc("/", home)

	log.Println("listening on", *addr)
	if err := http.ListenAndServe(*addr, nil); err != nil {
		log.Fatalf("ListenAndServe: %v", err)
	}
}

func home(w http.ResponseWriter, r *http.Request) {
	c, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Printf("ws upgrade error: %v", err)
		return
	}
	defer c.Close()

	go func() {
		_ = c.SetWriteDeadline(time.Now().Add(10 * time.Second))
		if err := c.WriteMessage(websocket.TextMessage, indexHTML); err != nil {
			log.Printf("write error: %v", err)
			return
		}
	}()

	for {
		_, _, err := c.ReadMessage()
		if err != nil {
			log.Printf("read: %v (closing handler)", err)
			return
		}
	}
}
