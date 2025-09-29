package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"os/signal"
	"strings"
	"sync"
	"syscall"
	"time"
)

// Сообщение, которое будет транслироваться всем
type chatMsg struct {
	From string
	Text string
	Time time.Time
}

// Описание подключенного пользователя
type client struct {
	Name string
	Conn net.Conn
	Out  chan string // буфер исходящих строк этому клиенту
}

type server struct {
	mu      sync.Mutex
	clients map[string]*client // по имени
	bcast   chan chatMsg       // общий канал трансляции
}

func newServer() *server {
	return &server{
		clients: make(map[string]*client),
		bcast:   make(chan chatMsg, 128),
	}
}

func (s *server) run(addr string) error {
	ln, err := net.Listen("tcp", addr)
	if err != nil {
		return err
	}
	defer ln.Close()

	fmt.Printf("Chat server listening on %s\n", addr)

	// Горутина-транслятор: читает из s.bcast и отправляет всем пользователям
	go s.broadcaster()

	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, os.Interrupt, syscall.SIGTERM)
	go func() {
		<-sigCh
		fmt.Println("\nShutting down...")
		ln.Close()
		s.mu.Lock()
		for _, c := range s.clients {
			c.Conn.Close()
		}
		s.mu.Unlock()
		os.Exit(0)
	}()

	for {
		conn, err := ln.Accept()
		if err != nil {
			if ne, ok := err.(net.Error); ok && !ne.Temporary() {
				return nil
			}
			fmt.Println("accept error:", err)
			continue
		}
		go s.handleConn(conn)
	}
}

func (s *server) handleConn(conn net.Conn) {
	defer conn.Close()
	r := bufio.NewScanner(conn)
	r.Buffer(make([]byte, 0, 1024), 64*1024)

	// 1) Первая строка — имя
	if !r.Scan() {
		return
	}
	name := strings.TrimSpace(r.Text())
	if name == "" {
		fmt.Fprintln(conn, "ERROR: empty name")
		return
	}
	// запретим служебные символы
	if strings.ContainsAny(name, " \t\r\n") || len(name) > 32 {
		fmt.Fprintln(conn, "ERROR: invalid name")
		return
	}

	// 2) Регистрируем клиента с уникальным именем
	c := &client{
		Name: name,
		Conn: conn,
		Out:  make(chan string, 64),
	}
	if !s.addClient(c) {
		fmt.Fprintln(conn, "ERROR: name already taken")
		return
	}
	defer s.removeClient(c.Name)

	// 3) Горутина отправки сообщений этому клиенту
	go s.writer(c)

	// 4) Приветствие и оповещение всех
	c.Out <- fmt.Sprintf("Welcome, %s! Commands: /who, /quit", c.Name)
	s.bcast <- chatMsg{From: "server", Text: fmt.Sprintf("%s joined", c.Name), Time: time.Now()}

	// 5) Чтение входящих сообщений от клиента
	for r.Scan() {
		line := strings.TrimSpace(r.Text())
		if line == "" {
			continue
		}
		switch line {
		case "/quit":
			c.Out <- "Bye!"
			return
		case "/who":
			c.Out <- "Online: " + strings.Join(s.listClients(), ", ")
			continue
		}
		// широковещательное сообщение
		s.bcast <- chatMsg{From: c.Name, Text: line, Time: time.Now()}
	}
	// Если сканер завершился клиент отключился
}

func (s *server) writer(c *client) {
	w := bufio.NewWriter(c.Conn)
	for msg := range c.Out {
		if _, err := w.WriteString(msg + "\n"); err != nil {
			return
		}
		if err := w.Flush(); err != nil {
			return
		}
	}
}

func (s *server) broadcaster() {
	for m := range s.bcast {
		line := fmt.Sprintf("[%s] %s: %s", m.Time.Format("15:04:05"), m.From, m.Text)
		s.mu.Lock()
		for _, c := range s.clients {
			// не блокируемся используем неблокирующую попытку записать в буфер
			select {
			case c.Out <- line:
			default:
				// если у клиента переполнен буфер скипаем сообщение
			}
		}
		s.mu.Unlock()
	}
}

func (s *server) addClient(c *client) bool {
	s.mu.Lock()
	defer s.mu.Unlock()
	if _, exists := s.clients[c.Name]; exists {
		return false
	}
	s.clients[c.Name] = c
	return true
}

func (s *server) removeClient(name string) {
	s.mu.Lock()
	c, ok := s.clients[name]
	if ok {
		delete(s.clients, name)
	}
	s.mu.Unlock()
	if ok {
		close(c.Out)
		_ = c.Conn.Close()
		s.bcast <- chatMsg{From: "server", Text: fmt.Sprintf("%s left", name), Time: time.Now()}
	}
}

func (s *server) listClients() []string {
	s.mu.Lock()
	defer s.mu.Unlock()
	out := make([]string, 0, len(s.clients))
	for name := range s.clients {
		out = append(out, name)
	}
	return out
}

func main() {
	srv := newServer()
	if err := srv.run(":8080"); err != nil {
		fmt.Println("server error:", err)
	}
}
