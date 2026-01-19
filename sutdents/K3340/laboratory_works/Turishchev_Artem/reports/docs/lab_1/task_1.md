# Задание 1

## Описание задачи

Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.

## Описание решения

Было реализовал простое клиент-серверное приложение на Python с использованием UDP сокетов для обмена сообщениями, с использованием библиотек socket

## Листинг кода

### server.py

```python
import socket
from config import HOST, PORT


conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
conn.bind((HOST, PORT))
data, addr = conn.recvfrom(1024)
msg = data.decode('utf-8')
print(f"recieved message: {msg}")
if msg == "Hello, server":
    ans_message = "Hello, client"
    conn.sendto(ans_message.encode(), addr)
else:
    print("Unknow message recieved")

conn.close()
```

### client.py

```python
import socket
from config import HOST, PORT

msg = "Hello, server"
conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
conn.connect((HOST, PORT))
conn.send(msg.encode())
response = conn.recv(1024)
print(f"response: {response.decode("utf-8")}")
```

### config.py

```python
HOST = "127.0.0.1"
PORT = 14900
```
