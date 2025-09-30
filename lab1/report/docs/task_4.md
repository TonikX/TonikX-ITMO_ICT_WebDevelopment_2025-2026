### Задание 4 (Многопользовательский чат, TCP + threading)
Сервер:
```bash
import socket
import threading


HOST = "localhost"
PORT = 12000


clients = {}
lock = threading.Lock()


def broadcast(sender_conn, message: bytes):
    with lock:
        for conn in list(clients.keys()):
            if conn is not sender_conn:
                try:
                    conn.sendall(message)
                except Exception:
                    try:
                        conn.close()
                    except Exception:
                        pass
                    clients.pop(conn, None)


def handle_client(conn, addr):
    with conn:
        conn.sendall("Введите имя: ".encode("utf-8"))
        name = b""
        while not name.endswith(b"\n"):
            chunk = conn.recv(4096)
            if not chunk:
                return
            name += chunk

        name = name.decode("utf-8", errors="replace").strip() or f"user_{addr[1]}"

        with lock:
            clients[conn] = name
        
        broadcast(conn, f"* {name} вошел в чат\n".encode("utf-8"))

        try:
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                text = data.decode("utf-8", errors="replace").rstrip("\n")
                if text.lower() == "/quit":
                    break
                msg = f"[{name}]: {text}\n".encode("utf-8")
                broadcast(conn, msg)
        finally:
            with lock:
                clients.pop(conn, None)
            broadcast(conn, f"* {name} вышел из чата\n".encode("utf-8"))


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"[CHAT SERVER] Listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            print(f"[CHAT SERVER] Connection from {addr}")
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    main()
```

```bash
python task4_chat/server_chat.py
```
Клиент (в разных терминалах несколько раз):
```bash 
import os
import socket
import threading
import sys

HOST = "localhost"
PORT = 12000

def reader(sock):
    while True:
        data = sock.recv(4096)
        if not data:
            print("\n[CLIENT] Соединение закрыто")
            os._exit(0)
        sys.stdout.write(data.decode("utf-8", errors="replace"))
        sys.stdout.flush()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        threading.Thread(target=reader, args=(s,), daemon=True).start()
        # имя
        name = input()
        s.sendall((name + "\n").encode("utf-8"))
        while True:
            line = input()
            if not line:
                continue
            s.sendall((line + "\n").encode("utf-8"))
            if line.strip().lower() == "/quit":
                break

if __name__ == "__main__":
    main()
```

```bash
python task4_chat/client_chat.py
```