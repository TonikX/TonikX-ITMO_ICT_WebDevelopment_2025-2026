# Задание 1: UDP-клиент и сервер

## Условие
Реализовать клиентскую и серверную часть приложения.  
Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера.  
В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.  

Требования:

- Использовать библиотеку `socket`.  
- Реализовать с помощью протокола *UDP*.  

---

## Код программы

### Сервер (server.py)

```python
import socket

HOST = "127.0.0.1"
PORT = 9999

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    print(f"[UDP SERVER] Listening on {HOST}:{PORT}")
    while True:
        data, addr = sock.recvfrom(1024)
        msg = data.decode("utf-8", errors="replace")
        print(f"[RECV from {addr}] {msg}")
        if msg.strip().lower() == "hello, server":
            sock.sendto(b"Hello, client", addr)
        else:
            sock.sendto(b"Unknown message", addr)

if __name__ == "__main__":
    main()
```

### Клиент (client.py)

```python
import socket
import sys

HOST = "127.0.0.1"
PORT = 9999
MESSAGE = "Hello, server"

def main():
    message = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else MESSAGE
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(3)
    sock.sendto(message.encode("utf-8"), (HOST, PORT))
    try:
        data, _ = sock.recvfrom(1024)
        print("[REPLY]", data.decode("utf-8", errors="replace"))
    except socket.timeout:
        print("No response (timeout).")

if __name__ == "__main__":
    main()
```

---

## Запуск

1. Открыть два терминала.  
2. В первом запустить сервер:  
   ```bash
   python server.py
   ```
3. Во втором запустить клиент:  
   ```bash
   python client.py
   ```
   По умолчанию отправляется сообщение `"Hello, server"`.  
   Можно передать собственное сообщение:  
   ```bash
   python client.py "test123"
   ```

---

## Результат

**Сервер:**
```
[UDP SERVER] Listening on 127.0.0.1:9999
[RECV from ('127.0.0.1', 54321)] Hello, server
```

**Клиент (по умолчанию):**
```
[REPLY] Hello, client
```

**Клиент (с другим сообщением):**
```
[REPLY] Unknown message
```

---

## Выводы

1. Реализовано взаимодействие клиента и сервера по протоколу UDP.  
2. Сообщения корректно передаются и обрабатываются.  
3. Добавлена обработка «неизвестных сообщений» и таймаут на стороне клиента.  
4. Использован минимальный и наглядный набор функций библиотеки `socket`.
