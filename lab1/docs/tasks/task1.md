## Постановка задачи

Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.

## Требования

Обязательно использовать библиотеку socket.
Реализовать с помощью протокола UDP.

## Решение — описание и код

Ниже приведены два файла: `client.go` и `server.go`. Они реализуют простое обменное взаимодействие по UDP: клиент отправляет сообщение серверу, сервер логирует входящее сообщение и отвечает обратно.

### client.go

```go
//go:build ignore
// +build ignore

package main

import (
	"log"
	"net"
	"time"
)

func main() {
	conn, err := net.Dial("udp", "127.0.0.1:9000")
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close()

	msg := []byte("hello, server!")
	conn.SetWriteDeadline(time.Now().Add(1 * time.Second))
	if _, err := conn.Write(msg); err != nil {
		log.Fatal("write:", err)
	}

	buf := make([]byte, 2048)
	conn.SetReadDeadline(time.Now().Add(2 * time.Second))
	n, err := conn.Read(buf)
	if err != nil {
		log.Println("read error:", err)
		return
	}
	log.Println("reply:", string(buf[:n]))
}
```

### server.go

```go
//go:build ignore
// +build ignore

package main

import (
	"context"
	"log"
	"net"
	"os"
	"os/signal"
	"sync"
)

type packet struct {
	data []byte
	addr net.Addr
}

func main() {
	pc, err := net.ListenPacket("udp", ":9000")
	if err != nil {
		log.Fatal(err)
	}
	defer pc.Close()

	ctx, cancel := context.WithCancel(context.Background())
	sig := make(chan os.Signal, 1)
	signal.Notify(sig, os.Interrupt)
	go func() {
		<-sig
		cancel()
		pc.Close()
	}()

	var bufPool = sync.Pool{
		New: func() any { b := make([]byte, 2048); return &b },
	}

	jobs := make(chan *packet)
	var wg sync.WaitGroup

	numWorkers := 2
	for i := 0; i < numWorkers; i++ {
		wg.Add(1)
		go func(workerID int) {
			defer wg.Done()
			for pkt := range jobs {
				select {
				case <-ctx.Done():
					return
				default:
				}

				// processing
				log.Printf("worker %d handling addr=%v len=%d data=%q", workerID, pkt.addr, len(pkt.data), pkt.data)

				select {
				case <-ctx.Done():
					return
				default:
					_, err := pc.WriteTo([]byte("hello, client!"), pkt.addr)
					if err != nil {
						log.Println("write error:", err)
					}
				}
			}
		}(i)
	}

readLoop:
	for {
		bptr := bufPool.Get().(*[]byte)
		n, addr, err := pc.ReadFrom(*bptr)
		if err != nil {
			select {
			case <-ctx.Done():
				break readLoop
			default:
				log.Println("read error:", err)
				bufPool.Put(bptr)
				continue
			}
		}

		data := append([]byte(nil), (*bptr)[:n]...)
		bufPool.Put(bptr)

		log.Printf("enqueue addr=%v len=%d ptr=%p", addr, n, &data)
		jobs <- &packet{data: data, addr: addr}
	}

	close(jobs)
	wg.Wait()
	log.Println("server stopped")
}
```

---

## Детали решения

**Почему UDP и `net.ListenPacket` / `net.Dial`:**
- В Go для низкоуровневой работы с UDP удобно использовать `net.ListenPacket` (сервер) и `net.Dial("udp", ...)` (клиент), которые дают простой интерфейс для отправки/приема датаграмм.

**Воркеры и канал задач:**
- Принята модель producer-consumer: основной цикл чтения ставит пакеты в `jobs` канал, воркеры (фиксированное количество `numWorkers`) обрабатывают их параллельно.
- Это упрощает масштабирование обработки и имитацию асинхронной работы.

**Обработка прерывания и отмена (`context` + signal):**
- Для корректного завершения слушателя реализовано перехватывание `os.Interrupt` (Ctrl+C). При получении сигнала контекст отменяется, `pc.Close()` вызывается, чтение прерывается, реплики воркеров завершают работу.

**Отправка ответа клиенту:**
- Сервер отвечает с помощью `pc.WriteTo([]byte("hello, client!"), pkt.addr)`, где `pkt.addr` — адрес отправителя, извлечённый из `ReadFrom`.

**Дедлайны на клиенте:**
- Клиент устанавливает `SetWriteDeadline` и `SetReadDeadline`, чтобы не блокироваться навечно в случае проблем сети.


## Как запускать и тестировать

1. В одной консоли запустите сервер:

```bash
go run server.go
```

2. В другой консоли запустите клиент:

```bash
go run client.go
```

3. Ожидаемое поведение:
- В логах сервера будет запись о приёме пакета и адресе клиента, например:

```
enqueue addr=127.0.0.1:XXXXX len=13 ptr=0xc0000xxxx0
worker 0 handling addr=127.0.0.1:XXXXX len=13 data="hello, server!"
```

- Клиент выведет ответ от сервера:

```
2025/09/22 12:00:00 reply: hello, client!
```


## Заключение

Задача реализована в виде простого UDP-клиент/сервер примера на Go. В решении учтены:
- корректная работа с датаграммами UDP,
- безопасная передача данных воркерам (копирование данных до передачи),
- управление жизненным циклом через `context` и обработку системного сигнала `Interrupt`,
- установка таймаутов на стороне клиента.