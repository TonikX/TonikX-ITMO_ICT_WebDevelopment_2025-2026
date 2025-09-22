## Постановка задачи

Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла index.html.

**Требования:**
- Обязательно использовать библиотеку socket.

---

### client.go

```go
//go:build ignore
// +build ignore

package main

import (
	"flag"
	"log"
	"net/url"
	"os"
	"os/signal"

	"github.com/gorilla/websocket"
)

var addr = flag.String("addr", "localhost:8080", "http service address")

func main() {
	flag.Parse()
	log.SetFlags(0)

	interrupt := make(chan os.Signal, 1)
	signal.Notify(interrupt, os.Interrupt)

	u := url.URL{Scheme: "ws", Host: *addr, Path: "/"}
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

	select {
	case <-done:
		goto done
	case <-interrupt:
		goto done
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
	default:
	}
}
```

### server.go

```go
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
```

### index.html

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
</head>
<body>
    <h1>Hello World!</h1>
</body>
</html>
```

---

## Детали решения

- Сервер читает файл `index.html` в память при старте и отдает его клиенту при веб-сокет-подключении.
- Клиент устанавливает WebSocket-соединение и получает HTML как текстовое сообщение.

## Заключение

Простой пример, который демонстрирует отдачу статической HTML-страницы по запросу через WebSocket. Для реального HTTP-сервера удобнее использовать обычный HTTP-ответ (`http.ServeFile`) без WebSocket, но использование WS здесь может быть полезно для демонстраций или специальных задач.

