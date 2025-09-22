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
