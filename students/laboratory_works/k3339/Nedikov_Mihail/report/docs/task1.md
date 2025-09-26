# Задача 1

## Цель

Реализовать клиентскую и серверную часть приложения с использованием библиотеки **socket** и протокола **UDP**.  
Клиент должен отправить серверу сообщение _«Hello, server»_, сервер выводит его у себя и отвечает _«Hello, client»_, которое отображается у клиента.

## Выполнение
В данной задаче реализована программа, где:
- **Клиент** отправляет строку `"Hello, server"` серверу по протоколу UDP.  
- **Сервер** принимает сообщение и выводит его в консоль.  
- В ответ сервер отправляет строку `"Hello, client"`, которая отображается у клиента.  


### Клиент

```python
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

request = "Hello, server"
client_socket.sendto(request.encode(), ("localhost", 8080))

response, address = client_socket.recvfrom(1024)

print(response.decode())
```

### Сервер

```python
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_socket.bind(("localhost", 8080))

while True:
    request, address = server_socket.recvfrom(1024)

    print(request.decode())

    response = "Hello, client"
    server_socket.sendto(response.encode(), address)
```

## Результат

При запуске сервер ожидает сообщения:
На стороне клиента:

```
Hello, client
```

На стороне сервера:

```
Hello, server
```

![](assets/task1.png)

## Вывод

Была успешно реализована простая клиент-серверная архитектура с использованием UDP-сокетов. Клиент отправляет сообщение серверу, сервер его принимает и отвечает клиенту.
