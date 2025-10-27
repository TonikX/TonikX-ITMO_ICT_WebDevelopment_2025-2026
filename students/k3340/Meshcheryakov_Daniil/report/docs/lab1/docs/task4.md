# Задание 4: Многопользовательский чат

## Условие
Реализовать многопользовательский чат.  
Каждый клиент подключается к серверу, вводит свой никнейм и может обмениваться сообщениями с другими пользователями.  

Требования:
- Использовать библиотеку `socket`.  
- Для многопользовательского чата — `threading`.  
- Протокол: *TCP*.  
- Дополнительно реализовать команду `/nickname`, позволяющую менять ник во время работы чата.  

---

## Код программы

### Сервер (server.py)

```python
import socket, threading

HOST = "127.0.0.1"
PORT = 9997
clients = {}  # {conn: nickname}

def broadcast(msg, exclude=None):
    """Рассылает сообщение всем клиентам, кроме exclude."""
    for c in list(clients):
        if c is exclude:
            continue
        try:
            c.sendall(msg.encode("utf-8"))
        except:
            c.close()
            clients.pop(c, None)

def handle(conn):
    with conn:
        conn.sendall("Ник: ".encode("utf-8"))
        nick = conn.recv(1024).decode().strip() or "anon"
        clients[conn] = nick
        broadcast(f"* {nick} вошёл в чат *\n")

        while True:
            data = conn.recv(1024)
            if not data:
                break
            msg = data.decode().strip()

            if msg == "/quit":
                break

            if msg.startswith("/nickname "):
                new_nick = msg.partition(" ")[2].strip()
                if new_nick:
                    old_nick = clients[conn]
                    clients[conn] = new_nick
                    broadcast(f"* {old_nick} сменил ник на {new_nick} *\n")
                else:
                    conn.sendall("❌ Использование: /nickname новый_ник\n".encode("utf-8"))
                continue

            broadcast(f"[{clients[conn]}] {msg}\n")

        broadcast(f"* {clients[conn]} вышел из чата *\n")
        clients.pop(conn, None)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[CHAT SERVER] {HOST}:{PORT}")
        while True:
            conn, _ = s.accept()
            threading.Thread(target=handle, args=(conn,), daemon=True).start()

if __name__ == "__main__":
    main()
```

### Клиент (client.py)

```python
import socket
import threading
import sys

HOST = "127.0.0.1"
PORT = 9997

def reader(sock, stop_event):
    """Поток чтения сообщений от сервера."""
    while not stop_event.is_set():
        try:
            data = sock.recv(4096)
            if not data:
                break
            print(data.decode("utf-8", errors="replace"), end="")
        except OSError:
            break

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        nickname = input("Введите ваш ник: ").strip()
        if not nickname:
            nickname = "anon"
        s.sendall(nickname.encode("utf-8"))

        stop_event = threading.Event()
        t = threading.Thread(target=reader, args=(s, stop_event))
        t.start()

        try:
            while True:
                line = sys.stdin.readline()
                if not line:
                    break
                s.sendall(line.encode("utf-8"))
                if line.strip().lower() == "/quit":
                    break
        except KeyboardInterrupt:
            pass

        stop_event.set()
        try:
            s.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass

        t.join()

if __name__ == "__main__":
    main()
```

---

## Запуск

1. Запустить сервер:  
   ```bash
   python server.py
   ```
2. В нескольких терминалах запустить клиентов:  
   ```bash
   python client.py
   ```
3. Ввести ник и начать переписку.  
4. Доступные команды:  
   - `/quit` — выход из чата  
   - `/nickname новый_ник` — смена никнейма  

---

## Результат

**Пример работы с тремя клиентами:**

```
* Alex вошёл в чат *
* Bob вошёл в чат *
[Alex] Привет!
[Bob] Здорово!
* Bob сменил ник на Bobby *
[Bobby] Теперь так лучше
```

---

## Выводы

1. Реализован многопользовательский чат на TCP-сокетах.  
2. Каждый клиент обрабатывается в отдельном потоке, что позволяет работать с несколькими пользователями одновременно.  
3. Реализовано хранение никнеймов в словаре `{соединение: ник}`.  
4. Добавлена возможность смены ника через команду `/nickname`.  
5. Реализована корректная обработка выхода пользователя через `/quit`.  
