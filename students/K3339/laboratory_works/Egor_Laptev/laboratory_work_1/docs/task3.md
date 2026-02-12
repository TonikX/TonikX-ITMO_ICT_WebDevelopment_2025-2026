## Задание 3:
Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла `index.html`.


### Используемые технологии:
- Python socket
- Протокол TCP
- HTTP/1.1

### Файлы:


**server.py**
```python
import socket

HOST = 'localhost'
PORT = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)
print(f"Server is running on {HOST}:{PORT}")

while True:
    conn, addr = sock.accept()
    print(f"Подключен клиент: {addr}")
    try:
        request = conn.recv(1024).decode()
        print(f"Запрос:\n{request}")

        try:
            with open("index.html", "r", encoding="utf-8") as f:
                html_content = f.read()
        except FileNotFoundError:
            html_content = "<h1>Файл index.html не найден</h1>"

        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type: text/html; charset=utf-8\r\n"
        response += f"Content-Length: {len(html_content.encode('utf-8'))}\r\n"
        response += "\r\n"
        response += html_content

        conn.sendall(response.encode('utf-8'))
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        conn.close()

```

**index.html**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Goofy Ass Page</title>
    <style>
        body {
            background: linear-gradient(135deg, #ff6ec4, #7873f5);
            font-family: "Comic Sans MS", cursive, sans-serif;
            color: #fff;
            text-align: center;
            margin: 0;
            padding: 0;
            overflow: hidden;
        }

        h1 {
            font-size: 4em;
            margin-top: 50px;
            animation: wobble 2s infinite;
        }

        @keyframes wobble {
            0% { transform: rotate(0deg); }
            25% { transform: rotate(5deg); }
            50% { transform: rotate(-5deg); }
            75% { transform: rotate(5deg); }
            100% { transform: rotate(0deg); }
        }

        p {
            font-size: 2em;
            animation: rainbowText 5s infinite;
        }

        @keyframes rainbowText {
            0% { color: #ff0000; }
            20% { color: #ff9900; }
            40% { color: #ffff00; }
            60% { color: #00ff00; }
            80% { color: #00ffff; }
            100% { color: #ff00ff; }
        }

        .bouncing {
            position: absolute;
            font-size: 3em;
            animation: bounce 3s infinite;
        }

        @keyframes bounce {
            0%, 100% { top: 10%; }
            50% { top: 70%; }
        }
    </style>
</head>
<body>
    <h1>HELLLOOO!!!</h1>
    <p>Welcome!</p>

    <div class="bouncing" style="left:10%;">🤪</div>
    <div class="bouncing" style="left:40%; animation-delay: 1s;">🦄</div>
    <div class="bouncing" style="left:70%; animation-delay: 2s;">🍕</div>
</body>
</html>

```

### Результат работы:
Сервер:
```
Server is running on localhost:8080
Подключен клиент: ('127.0.0.1', 53214)
Запрос:
GET / HTTP/1.1
Host: localhost:8080
...

```
Клиент:
Отображается HTML-страница
