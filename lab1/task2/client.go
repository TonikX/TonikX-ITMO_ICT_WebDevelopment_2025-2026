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
