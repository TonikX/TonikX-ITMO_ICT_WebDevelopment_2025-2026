# Задание
Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее
HTML-страницу, которая сервер подгружает из файла index.html.

**Требования:**

- Обязательно использовать библиотеку socket.
 
***

# Решение

## Сервер

```python
import socket

HOST = '127.0.0.1'
PORT = 9090

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen(1)

print(f'Сервер запущен на {HOST}:{PORT}')


while True:
    client_connection, client_address = server_socket.accept()

    with open('index.html', 'r', encoding='UTF-8') as html_file:
        html_content = html_file.read()

    content_length = len(html_content.encode('utf-8'))

    http_response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=UTF-8\r\n"
        f"Content-Length: {content_length}\r\n"
        "Connection: close\r\n"
        "\r\n"
        + html_content
    )

    client_connection.sendall(http_response.encode('UTF-8'))

    client_connection.close()
```

Страница, которую выдаёт сервер:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Простой сервер на Python</title>
</head>
<body>
    <h1>Привет! Это простая HTML-страница.</h1>
    <p>Этот сервер написан на Python и работает через сокеты.</p>
</body>
</html>
```

***

# Пояснение

Создаём TCP сокет на сервере, используя адрес `127.0.0.1` и порт `9090` и устанавливаем соединение с клиентом.
Далее считываем файл index.html, формируем ответ `200 OK` и отправляем его клиенту.

Браузер отправляет HTTP GET запрос серверу и получает в ответ HTTP-сообщение, содержащее
HTML-страницу index.html.