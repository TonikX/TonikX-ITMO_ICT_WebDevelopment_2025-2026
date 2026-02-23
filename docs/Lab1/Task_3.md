# Задание 3

## Задание:

Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла index.html.

### Выполнение:

**server_3.py**

```
    import socket

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind(('localhost', 1234))
    server_socket.listen(1)
```

Создаём TCP-сокет `(SOCK_STREAM)`, так как HTTP использует TCP.

```
    while True:
        client_socket, address = server_socket.accept()

        data = client_socket.recv(1024).decode()
        print("request:\n", data)
        try:
            with open('index.html', 'r', encoding='utf-8') as f:
                html = f.read()

            http_response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=UTF-8\r\n"
                f"Content-Length: {len(html.encode('utf-8'))}\r\n"
                "Connection: close\r\n"
                "\r\n"
                f"{html}"
            )
```
Принимаем запрос от клиента - `recv(1024)`

Открываем файл `index.html` и читает его содержимое.

Далее формирует HTTP-ответ:

`200 OK` — успешный запрос;

`Content-Type: text/html` — указывает, что ответ содержит HTML-страницу;

`Content-Length` — размер содержимого в байтах;

`Connection: close` — сервер закрывает соединение после ответа.


```
    except:
        http_response = (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            "Connection: close\r\n"
            "\r\n"
            "<h1>404 — file index.html not found</h1>"
            )
```

Если файл `index.html` не найден, сервер отправит ошибку 404.

```
    client_socket.sendall(http_response.encode())
    client_socket.close()
```

Отправляет сформированный HTTP-ответ клиенту.

Закрывает соединение с клиентом.

**index.html**

```
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Здравствуйте, сервер запущен</title>
        <style>
            body {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                font-size: 24px;
            }
        </style>
    </head>
    <body>
        Привет
    </body>
    </html>
```

#### Результаты:

**Сервер**

![1](../img/task_3.1.png)

**Страница**

![2](../img/task3.2.png)


