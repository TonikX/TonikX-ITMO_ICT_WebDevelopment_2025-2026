## Цель

Реализовать серверную часть приложения, которая обрабатывает HTTP-запросы.  
Клиент подключается к серверу и получает в ответ **HTTP-сообщение**, содержащее HTML-страницу, загруженную сервером из файла `index.html`.

## Выполнение

В этой задаче нужно было построить простейший веб-сервер на основе **сокетов**.  
Я использовал протокол **TCP**, так как именно он применяется в HTTP. На стороне сервера я создал сокет через метод `socket()`, затем привязал его к адресу и порту (`bind()`) и перевёл в режим ожидания входящих соединений (`listen()`).

Когда клиент подключается (`accept()`), сервер получает HTTP-запрос и открывает файл `index.html`, находящийся в той же папке, что и сам скрипт. Содержимое файла читается и формируется в ответ: заголовки `HTTP/1.1 200 OK`, `Content-Type`, `Content-Length`, а затем идёт сам HTML-код. Этот ответ сервер отправляет клиенту методом `sendall()`.

На стороне клиента я также создал TCP-сокет и подключился к серверу через `connect()`. Затем клиент отправляет HTTP-запрос вида `GET / HTTP/1.1`. Сервер возвращает полноценный HTTP-ответ, который клиент выводит в консоль.

Таким образом, удалось реализовать минимальный аналог веб-сервера, который умеет отдавать HTML-страницу.

### Сервер

```python
import socket
import os

# Параметры сервера
HOST = 'localhost'
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "index.html")

while True:
    client_connection, client_address = server_socket.accept()
    print(f'Подключение от {client_address}')

    request = client_connection.recv(1024).decode()
    print(f'Запрос клиента:\\n{request}')

    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    http_response = (
        "HTTP/1.1 200 OK\\r\\n"
        "Content-Type: text/html; charset=UTF-8\\r\\n"
        f"Content-Length: {len(html_content.encode('utf-8'))}\\r\\n"
        "Connection: close\\r\\n"
        "\\r\\n"
        + html_content
    )

    client_connection.sendall(http_response.encode("utf-8"))
    client_connection.close()
```

### Клиент

```python
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 8080))

request = "GET / HTTP/1.1\\r\\nHost: localhost\\r\\n\\r\\n"
client_socket.sendall(request.encode())

response = client_socket.recv(1024).decode()

print("=== Ответ сервера ===")
print(response)

client_socket.close()

```

## Результат

При запуске клиент отправляет HTTP-запрос:

```
GET / HTTP/1.1
Host: localhost
```

Сервер возвращает HTTP-ответ вместе с HTML-кодом из файла index.html

```
HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Length: ...
Connection: close

<html> ... </html>

```

![](assets/task3.png)

## Вывод

В результате удалось создать минимальный HTTP-сервер на сокетах, который корректно отдаёт HTML-страницу по запросу клиента.
Это демонстрирует базовые принципы работы веб-серверов и взаимодействия по протоколу HTTP.
