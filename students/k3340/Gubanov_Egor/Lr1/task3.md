# Задание 3: HTTP Файловый Сервер

## Практическое задание

Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла index.html.

### Требования:
- Обязательно использовать библиотеку `socket`

### Полезные ссылки:
- [ZetCode: Работа с сокетами](https://zetcode.com/python/socket/)

---

## Реализация

### Сервер (task3/server.py)

```python
import socket
import os
from datetime import datetime

def create_http_response(status_code, body, content_type='text/html; charset=utf-8'):
    """Создает HTTP ответ с заданным статус-кодом и телом"""
    status_text = {
        200: "200 OK",
        404: "404 Not Found", 
        405: "405 Method Not Allowed"
    }.get(status_code, "500 Internal Server Error")
    
    headers = [
        f"HTTP/1.1 {status_text}",
        f"Server: SimpleHTTPServer/1.0",
        f"Content-Type: {content_type}",
        f"Content-Length: {len(body)}",
        f"Date: {datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}",
        "Connection: close",
        "",
        ""
    ]
    return "\r\n".join(headers).encode('utf-8') + body

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('127.0.0.1', 8003))
        server_socket.listen(5)
        
        print("HTTP Сервер")
        print("=" * 20)
        print(f"Сервер запущен на http://127.0.0.1:8003/")
        print(f"Файл: index.html")
        print(f"Протокол: HTTP/1.1")
        print("\nНажмите Ctrl+C для остановки...")
        
        try:
            while True:
                conn, addr = server_socket.accept()
                with conn:
                    try:
                        request = conn.recv(1024).decode('utf-8')
                        if not request:
                            continue
                            
                        lines = request.splitlines()
                        if not lines:
                            continue
                            
                        first_line = lines[0]
                        parts = first_line.split()
                        if len(parts) < 3:
                            continue
                            
                        method, path, version = parts
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] {addr} -> {method} {path}")
                        
                        if method == 'GET' and path == '/':
                            if os.path.exists('index.html'):
                                with open('index.html', 'r', encoding='utf-8') as f:
                                    html_content = f.read()
                                response = create_http_response(200, html_content.encode('utf-8'))
                            else:
                                error_html = """
                                <!DOCTYPE html>
                                <html><head><title>404 Not Found</title></head>
                                <body><h1>404 Not Found</h1>
                                <p>Файл index.html не найден</p>
                                <p>Создайте файл index.html в папке с сервером</p>
                                </body></html>
                                """
                                response = create_http_response(404, error_html.encode('utf-8'))
                        else:
                            error_html = """
                            <!DOCTYPE html>
                            <html><head><title>405 Method Not Allowed</title></head>
                            <body><h1>405 Method Not Allowed</h1>
                            <p>Метод не поддерживается</p>
                            <p><a href="/">Вернуться на главную</a></p>
                            </body></html>
                            """
                            response = create_http_response(405, error_html.encode('utf-8'))
                        
                        conn.sendall(response)
                        
                    except Exception as e:
                        print(f"Ошибка обработки запроса от {addr}: {e}")
                        
        except KeyboardInterrupt:
            print("\nСервер остановлен")

if __name__ == "__main__":
    run_server()
```

### HTML файл (task3/index.html)

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HTTP Сервер</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .container {
            background: white;
            border-radius: 15px;
            padding: 2rem;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            max-width: 500px;
        }
        
        h1 {
            color: #333;
            margin-bottom: 1rem;
            font-size: 2rem;
        }
        
        .status {
            background: #f0f8ff;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            border-left: 4px solid #667eea;
        }
        
        .info {
            color: #666;
            line-height: 1.6;
            margin: 1rem 0;
        }
        
        .tech {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 0.5rem;
            margin: 1rem 0;
        }
        
        .tech span {
            background: #667eea;
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 15px;
            font-size: 0.8rem;
        }
        
        .footer {
            margin-top: 1.5rem;
            padding-top: 1rem;
            border-top: 1px solid #eee;
            color: #999;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌐 HTTP Сервер</h1>
        
        <div class="status">
            ✅ Сервер работает корректно<br>
            📁 Файл index.html загружен<br>
            🔗 Протокол HTTP/1.1
        </div>
        
        <div class="info">
            <p>Этот сервер успешно загрузил HTML страницу из файла <code>index.html</code> и отправил её по HTTP протоколу.</p>
        </div>
        
        <div class="tech">
            <span>Python</span>
            <span>Socket</span>
            <span>HTTP/1.1</span>
            <span>HTML</span>
        </div>
        
        <div class="footer">
            <p>Лабораторная работа №1 - Сетевые технологии</p>
            <p>Губанов Егор, группа K3340</p>
        </div>
    </div>
</body>
</html>
```

## Запуск

1. Убедитесь, что файл `index.html` находится в той же папке, что и `server.py`
2. Запустите сервер:
   ```bash
   python task3/server.py
   ```
3. Откройте браузер и перейдите по адресу: http://127.0.0.1:8000

## Результат

**Сервер:**
```
HTTP Сервер
====================
Сервер запущен на http://127.0.0.1:8000/
Файл: index.html
Протокол: HTTP/1.1

Нажмите Ctrl+C для остановки...
[14:30:15] ('127.0.0.1', 54321) -> GET /
```

**Браузер:**
Отображается красивая HTML страница с информацией о сервере.

## Выводы

1. Реализован простой HTTP сервер без использования внешних библиотек
2. Сервер корректно обрабатывает GET запросы и возвращает HTML страницы
3. Добавлена обработка ошибок 404 и 405
4. HTTP заголовки формируются в соответствии со стандартом
5. Сервер поддерживает кириллицу в HTML контенте
