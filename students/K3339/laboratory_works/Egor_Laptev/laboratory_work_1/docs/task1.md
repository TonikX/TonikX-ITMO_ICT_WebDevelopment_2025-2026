## Задание 1:
Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.


### Используемые технологии:
- Python socket
- Протокол UDP

### Файлы:

**client.py**
```python 
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

HOST = 'localhost'
PORT = 8080

sock.sendto(b'Hello, server!', (HOST, PORT))

data, addr = sock.recvfrom(1024)
sock.close()

print(data.decode())
```

**server.py**
```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

PORT = 8080

sock.bind(('', PORT))

print("[UDP] Server is running on port {}".format(PORT))

while True:
    data, addr = sock.recvfrom(1024)
    print(f"Получено от {addr}: {data.decode()}")

    sock.sendto(b'Hello, client', addr)

```

### Результат работы:
Сервер выводит на консоль:
```
[UDP] Server is running on port 8080
Получено от ('127.0.0.1', 12345): Hello, server!
```
Клиент выводит на консоль:

```
Hello, client
```

