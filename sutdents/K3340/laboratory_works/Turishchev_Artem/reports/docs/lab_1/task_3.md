# Задание 3

## Описание задачи

Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла index.html.

## Описание решения

Был реализован простой HTTP-сервер на Python с использованием TCP сокетов для отдачи HTML-страницы, с использованием библиотек socket

## Листинг кода

### server.py

```python
import socket
from config import HOST, PORT

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.bind((HOST, PORT))
conn.listen(10)

while True:
    try:
        client_socket, addr = conn.accept()
        data = client_socket.recv(16384).decode()
        print("получен запрос:", data)

        response_type = "HTTP/1.1 200 OK\r\n"
        headers = "Content-Type: text/html; charset=utf-8\r\n\r\n"
        with open("index.html", encoding="utf-8") as file:
            body = file.read()
        msg = response_type + headers + body
        client_socket.send(msg.encode())
        client_socket.close()

    except KeyboardInterrupt:
        conn.close()
        break
```

### config.py

```python
HOST = "127.0.0.1"
PORT = 14900
```
