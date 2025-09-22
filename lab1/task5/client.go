//go:build ignore
// +build ignore

package main

import (
	"encoding/json"
	"flag"
	"io"
	"log"
	"net/http"
	"net/url"
	"time"

	"github.com/gorilla/websocket"
)

var addr = flag.String("addr", "localhost:8081", "http service address")

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

	// 1) отправим одну оценку через /stats/add
	u := url.URL{Scheme: "ws", Host: *addr, Path: "/stats/add"}
	c, _, err := websocket.DefaultDialer.Dial(u.String(), nil)
	if err != nil {
		log.Fatal("dial:", err)
	}
	defer c.Close()

	req := statIn{Subject: "Math", Value: 5}
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

	h := "http://" + *addr + "/"
	resp, err := http.Get(h)
	if err != nil {
		log.Println("fetch / error:", err)
	} else {
		b, _ := io.ReadAll(resp.Body)
		_ = resp.Body.Close()
		log.Printf("got index.html, %d bytes\n", len(b))
	}

	// 3) подключимся к /stats и прочитаем снимок
	u2 := url.URL{Scheme: "ws", Host: *addr, Path: "/stats"}
	c2, _, err := websocket.DefaultDialer.Dial(u2.String(), nil)
	if err != nil {
		log.Fatal("dial stats:", err)
	}
	defer c2.Close()

	_, p, err := c2.ReadMessage()
	if err != nil {
		log.Fatal("read stats:", err)
	}
	var arr []statOut
	if err := json.Unmarshal(p, &arr); err != nil {
		log.Fatal("unmarshal stats:", err)
	}
	log.Printf("stats: %+v\n", arr)
}
