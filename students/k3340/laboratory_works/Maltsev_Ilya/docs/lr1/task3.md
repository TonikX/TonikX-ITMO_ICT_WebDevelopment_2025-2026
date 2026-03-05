# Задание 3

## Описание

Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла index.html.

## Стек

- Язык: Python
- Библиотека: socket
- Протокол: TCP

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

server.py

```python
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('localhost', 8080))

server_socket.listen(1)
print("Сервер запущен на порту 8080...")

while True:
    client_connection, client_address = server_socket.accept()
    print(f'Подключение от {client_address}')

    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    response = f"HTTP/1.1 200 OK\nContent-Type: text/html; charset=UTF-8\nContent-Length: {len(content)}\n\n{content}"
    client_connection.sendall(response.encode())

    client_connection.close()
```

index.html
```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-16">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-16">
    <title>Lab1</title>
</head>
<body>
    <h1>Задание 3</h1>
    <h2>Мальцев Илья</h2>
</body>
</html>

```

## Скриншоты
![img_3.png](images/img_3.png)