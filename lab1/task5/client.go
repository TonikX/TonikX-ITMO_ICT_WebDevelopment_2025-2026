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
