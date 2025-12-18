# Задание 1: UDP Клиент-Сервер

## Задача

Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно
отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно
отобразиться у клиента.

## Реализация

Для решения использовался протокол **UDP**, поэтому сокеты создавались с типом `socket.SOCK_DGRAM`. Сервер привязывался
к адресу и порту (`localhost:9999`) и в цикле ожидал данные (`recvfrom`). Клиент просто отправлял данные на известный
адрес
сервера (`sendto`), после чего ожидал ответ.

### server.py

```python
import socket

# AF_INET - IPv4, SOCK_DGRAM - UDP
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = ('localhost', 9999)
message = "Hello, server"

udp_socket.sendto(message.encode('utf-8'), addr)
print(f"Отправил: '{message}'")

data, server = udp_socket.recvfrom(1024)

print(f"Получил ответ: '{data.decode('utf-8')}'")
```

### client.py

```python
import socket

# AF_INET - IPv4, SOCK_DGRAM - UDP
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = ('localhost', 9999)
message = "Hello, server"

udp_socket.sendto(message.encode('utf-8'), addr)
print(f"Отправил: '{message}'")

data, server = udp_socket.recvfrom(1024)

print(f"Получил ответ: '{data.decode('utf-8')}'")
```