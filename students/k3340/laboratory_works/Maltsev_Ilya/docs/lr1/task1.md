# Задание 1

## Описание

Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», которое должно отображаться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое отображается у клиента.

## Стек

- Язык: Python
- Библиотека: socket
- Протокол: UDP

## Как запускать

1. Сервер:
    ```bash
    python3 server.py
    ```
2. Клиент:
    ```bash
    python3 client.py
    ```
   

## Код

client.py

```python
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(('localhost', 8080))

client_socket.sendall(b'Hello, server!')

response = client_socket.recv(1024)
print(f'Ответ от сервера: {response.decode()}')

client_socket.close()
```

server.py
```python
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(('localhost', 8080))

client_socket.sendall(b'Hello, server!')

response = client_socket.recv(1024)
print(f'Ответ от сервера: {response.decode()}')

client_socket.close()
```

## Скриншоты
![img.png](images/img.png)