# Задание 3: HTTP-сервер для возврата HTML-страницы
## Описание задания
Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла index.html.

## Ход выполнения
### Серверная часть (task_3_server.py):
```python
import socket
import os

def load_html_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "<html><body><h1>404 - File Not Found</h1></body></html>"

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('localhost', 8080)
    server_socket.bind(server_address)
    server_socket.listen(5)
    
    print(f"HTTP-сервер запущен на http://{server_address[0]}:{server_address[1]}")
    
    while True:
        try:
            client_socket, client_address = server_socket.accept()
            print(f"Подключился клиент: {client_address}")
            
            request = client_socket.recv(1024).decode('utf-8')
            print(f"Получен запрос:\n{request}")
            
            html_content = load_html_file('index.html')
            
            response_headers = [
                'HTTP/1.1 200 OK',
                'Content-Type: text/html; charset=utf-8',
                f'Content-Length: {len(html_content)}',
                'Connection: close',
                '\r\n'
            ]
            
            response = '\r\n'.join(response_headers) + html_content
            client_socket.sendall(response.encode('utf-8'))
            print("Отправлен HTTP-ответ с содержимым index.html")
            
            client_socket.close()
            
        except KeyboardInterrupt:
            break
```
### HTML-страница (index.html):
```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Тестовая страница</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        h1 { color: #333; text-align: center; }
        .container { background-color: white; padding: 20px; border-radius: 8px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Добро пожаловать на HTTP-сервер Королькова Артема!</h1>
        <p>Это тестовая страница, загружаемая сервером из файла index.html</p>
        <p>Сервер реализован на чистом Python с использованием библиотеки socket</p>
    </div>
</body>
</html>
```
## Вывод по заданию 3
Реализован простой HTTP-сервер, способный обслуживать HTML-страницы. Сервер корректно формирует HTTP-заголовки и возвращает содержимое файла index.html. Достигнута основа для понимания работы веб-серверов на низком уровне.
