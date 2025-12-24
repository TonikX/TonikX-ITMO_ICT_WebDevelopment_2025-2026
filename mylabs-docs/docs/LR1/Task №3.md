# Реализация сервера с HTML-страницей

## Условие задания  
Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла `index.html`.

**Требования:**  
- Использовать библиотеку `socket`. 

## Алгоритм решения  
- Сервер создаёт TCP-сокет и привязывает его к адресу `('localhost', 8080)`.  
- Сервер переходит в режим прослушивания входящих подключений (`listen`).  
- Клиент создаёт TCP-сокет и подключается к серверу.  
- Клиент отправляет HTTP-запрос для получения страницы.  
- Сервер принимает запрос от клиента (`recv`).  
- Сервер открывает файл `index.html` и считывает его содержимое.  
- Сервер формирует HTTP-ответ с заголовками (`200 OK`, `Content-Type`, `Content-Length`) и включённым HTML-контентом.  
- Сервер отправляет ответ клиенту (`sendall`).  
- Сервер закрывает соединение с клиентом, клиент получает ответ и выводит HTML-страницу.

## Код сервера
```python
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('localhost', 8080))

server_socket.listen(1)

while True:
    client_connection, client_address = server_socket.accept()

    request = client_connection.recv(1024).decode()

    with open('index.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(html_content.encode('utf-8'))}\r\n"
        "Connection: close\r\n"
        "\r\n" +
        html_content
    )

    client_connection.sendall(response.encode('utf-8'))

    client_connection.close()
```

## Код клиента
```python
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(('localhost', 8080))

http_request = "GET / HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n"
client_socket.sendall(http_request.encode('utf-8'))

response = b""
while True:
    chunk = client_socket.recv(4096)
    if not chunk:
        break
    response += chunk

print(response.decode('utf-8'))

client_socket.close()
```

## Результат работы
```html
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 222
Connection: close

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Моя страница</title>
</head>
<body>
    <h1>Привет! Это страница с сервера на Python.</h1>
</body>
</html>
```