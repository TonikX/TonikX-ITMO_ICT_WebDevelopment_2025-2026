# Отчет по заданию 3: HTTP сервер с отдачей HTML-страницы

## Цель работы
Реализовать серверную часть приложения, которая при подключении клиента возвращает HTTP-сообщение с HTML-страницей, загружаемой из файла index.html.

## Код программы

### server.py
```python
import socket

HOST = "127.0.0.1"
PORT = 8000

with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

http_response = f"""HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: {len(html_content.encode("utf-8"))}

{html_content}"""

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Сервер запущен на http://{HOST}:{PORT}")
    
    while True:
        conn, addr = server_socket.accept()
        with conn:
            request = conn.recv(1024).decode("utf-8")
            print("Запрос клиента:\n", request)
            # Отправляем ответ
            conn.sendall(http_response.encode("utf-8"))
```

### index.html
```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Мой сервер</title>
</head>
<body>
    <h1>Привет! Это страница, отданная через socket-сервер.</h1>
</body>
</html>
```

## Описание работы программы
### Серверная часть:
* Создает TCP-сокет с помощью socket.socket(socket.AF_INET, socket.SOCK_STREAM)
* Привязывает сокет к локальному адресу и порту 8000 с помощью bind()
* Загружает HTML-страницу из файла index.html в переменную html_content
* Формирует полный HTTP-ответ с правильными заголовками:
* Статус ответа: HTTP/1.1 200 OK
* Тип контента: text/html; charset=utf-8
* Длина контента: вычисляется автоматически
* Ожидает подключения клиентов с помощью listen()
* При подключении клиента принимает HTTP-запрос и отправляет подготовленный HTTP-ответ
### Особенности реализации:
* Используется кодировка UTF-8 для корректного отображения русского текста
* Content-Length вычисляется правильно с учетом кодировки
* HTTP-ответ формируется согласно стандарту HTTP/1.1
