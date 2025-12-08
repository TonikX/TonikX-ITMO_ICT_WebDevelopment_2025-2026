# Отчёт по заданию: UDP клиент-сервер на Python

## Цель
Создать простое клиент-серверное приложение с использованием протокола UDP. Клиент отправляет сообщение серверу, а сервер отвечает обратно.

---

## Файлы проекта

### 1. `server.py`

```python
import socket

HOST = "127.0.0.1" 
PORT = 12345        

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print(f"Сервер запущен на {HOST}:{PORT} и ждет сообщения...")

while True:
    data, addr = server_socket.recvfrom(1024)
    message = data.decode("utf-8")
    print(f"Получено от клиента {addr}: {message}")

    if message == "Hello, server":
        reply = "Hello, client"
        server_socket.sendto(reply.encode("utf-8"), addr)
```

### 2. `client.py`

```python
import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = "Hello, server"
client_socket.sendto(message.encode("utf-8"), (SERVER_HOST, SERVER_PORT))

data, _ = client_socket.recvfrom(1024)
print("Ответ от сервера:", data.decode("utf-8"))

client_socket.close()
```

## Серверная часть:
Создает UDP-сокет с помощью socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

Привязывает сокет к локальному адресу и порту с помощью bind()

В бесконечном цикле ожидает получение данных от клиентов

При получении сообщения "Hello, server" отправляет ответ "Hello, client"

## Клиентская часть:
Создает UDP-сокет

Отправляет сообщение "Hello, server" на сервер

Ожидает и выводит ответ от сервера

Закрывает соединение