# Лабораторная работа №1

## Задание 1. UDP клиент–сервер

**Условие:**  
Реализовать клиентскую и серверную часть приложения.  
Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера.  
В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.  

**Требования:**  
- Использовать библиотеку `socket`.  
- Реализовать с помощью протокола UDP.  

### Код сервера
```python
import socket
import threading

HOST = "127.0.0.1"
PORT = 5005

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print(f"UDP сервер запущен на {HOST}:{PORT}")

def handle_client(data, addr):
    print(f"Клиент {addr} сказал:", data.decode())
    reply = "Hello, client"
    server_socket.sendto(reply.encode(), addr)

while True:
    data, addr = server_socket.recvfrom(1024)
    thread = threading.Thread(target=handle_client, args=(data, addr))
    thread.start()
```

### Код клиента
```python
import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5005

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = "Hello, server"
client_socket.sendto(message.encode(), (SERVER_HOST, SERVER_PORT))

data, _ = client_socket.recvfrom(1024)
print("Сервер ответил:", data.decode())

client_socket.close()
```

**Вывод:**
В результате выполнения задания был реализован клиент–сервер на UDP.
Сервер принимает сообщение от клиента и отвечает на него.


## Задание 2. TCP: математическая операция

**Условие:**  
Реализовать клиентскую и серверную часть приложения.
Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры.
Сервер обрабатывает данные и возвращает результат клиенту.  

**Мой вариант:** №4 (площадь параллелограмма).

**Требования:**  
- Использовать библиотеку `socket`.  
- Реализовать с помощью протокола TCP.  

### Код сервера
```python
import socket
import threading

HOST = "127.0.0.1"
PORT = 8080

def handle_client(conn, addr):
    print(f"Подключился {addr}")
    request = conn.recv(1024).decode()
    print("Запрос:\n", request)

    try:
        with open("index.html", "r", encoding="utf-8") as f:
            body = f.read()
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(body.encode('utf-8'))}\r\n"
            "Connection: close\r\n"
            "\r\n"
            f"{body}"
        )
    except FileNotFoundError:
        response = "HTTP/1.1 404 Not Found\r\n\r\n<h1>404 Not Found</h1>"

    conn.sendall(response.encode("utf-8"))
    conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"HTTP сервер запущен на http://{HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
```

### Код клиента
```python
import socket

HOST = "127.0.0.1"
PORT = 5006

a = input("Введите основание параллелограмма: ")
h = input("Введите высоту параллелограмма: ")

message = f"{a} {h}"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
client_socket.send(message.encode())

data = client_socket.recv(1024).decode()
print("Ответ от сервера:", data)

client_socket.close()
```

**Вывод:**
В результате выполнения задания реализован TCP-сервер, который получает от клиента параметры параллелограмма и возвращает рассчитанную площадь.


## Задание 3. HTTP-сервер

**Условие:**  
Реализовать серверную часть приложения. Клиент подключается к серверу и получает HTTP-сообщение с HTML-страницей, которая подгружается из файла `index.html` 

**Требования:**  
- Использовать библиотеку `socket`.  

### Код сервера
```python
import socket

HOST = "127.0.0.1"
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Сервер запущен на http://{HOST}:{PORT}")

while True:
    conn, addr = server_socket.accept()
    print(f"Подключился клиент {addr}")

    request = conn.recv(1024).decode()
    print("Запрос:\n", request)

    try:
        with open("index.html", "r", encoding="utf-8") as f:
            body = f.read()
    except FileNotFoundError:
        body = "<h1>Файл index.html не найден</h1>"

    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body.encode('utf-8'))}\r\n"
        "Connection: close\r\n"
        "\r\n"
        f"{body}"
    )

    conn.sendall(response.encode("utf-8"))
    conn.close()
```

### Код клиента
```python
import socket

HOST = "127.0.0.1"
PORT = 8080

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

request = "GET / HTTP/1.1\r\nHost: 127.0.0.1\r\nConnection: close\r\n\r\n"
client_socket.send(request.encode())

response = b""
while True:
    data = client_socket.recv(1024)
    if not data:
        break
    response += data

client_socket.close()

print(response.decode())
```

### HTML-страница
```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Мой первый сервер</title>
    <style>
        body {
            margin: 0;
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: #fff;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            text-align: center;
        }
        .card {
            background: rgba(0, 0, 0, 0.3);
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
            max-width: 600px;
        }
        h1 {
            font-size: 2.5rem;
            margin-bottom: 20px;
        }
        p {
            font-size: 1.2rem;
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>Добро пожаловать на мой сервер!</h1>
        <p>Эта HTML-страница</p>
    </div>
</body>
</html>
```

**Вывод**
В результате был создан простой HTTP-сервер на Python, который отдаёт клиенту HTML-страницу.


## Задание 4. Многопользовательский чат

**Условие:**  
Реализовать двухпользовательский или многопользовательский чат.
Для максимального количества баллов реализовать многопользовательский чат.

**Требования:**  
- Использовать библиотеку `socket`.
- Для многопользовательского чата использовать библиотеку `threading`.
- Реализация на TCP: обработка подключений и сообщений пользователей в потоках.

### Код сервера
```python
import socket
import threading

HOST = "127.0.0.1"
PORT = 5007

clients = []
nicknames = []

def broadcast(message, sender_socket=None):
    for client in clients:
        if client != sender_socket:
            client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if not message:
                break

            index = clients.index(client)
            nickname = nicknames[index]
            full_message = f"[{nickname}]: {message}\n"
            print(full_message.strip())
            broadcast(full_message.encode("utf-8"), client)

        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames.pop(index)
                broadcast(f"{nickname} покинул чат.\n".encode("utf-8"))
            break

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Сервер запущен на {HOST}:{PORT}")

    while True:
        client, addr = server.accept()
        print(f"Подключение от {addr}")

        client.send("Введите ваш никнейм: ".encode("utf-8"))
        nickname = client.recv(1024).decode("utf-8")

        clients.append(client)
        nicknames.append(nickname)

        print(f"Пользователь {nickname} подключился.")
        broadcast(f"{nickname} присоединился к чату!\n".encode("utf-8"))
        client.send("Вы подключены к чату!\n".encode("utf-8"))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    start_server()
```

### Код клиента
```python
import socket
import threading
import sys

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode("utf-8")
            if not msg:
                break
            print(msg)
        except:
            print("Соединение с сервером потеряно.")
            break

def main():
    host = "127.0.0.1"   
    port = 5007        

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((host, port))
    except ConnectionRefusedError:
        print(f"Не удалось подключиться к серверу {host}:{port}. "
            "Проверь, что сервер запущен.")
        sys.exit(1)
    except socket.error as e:
        print(f"Ошибка подключения: {e}")
        sys.exit(1)

    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

    print("Подключено к чату. Напишите сообщение (или 'exit' для выхода).")

    while True:
        msg = input()
        if msg.lower() == "exit":
            sock.close()
            break
        try:
            sock.send(msg.encode("utf-8"))
        except:
            print("Не удалось отправить сообщение. Соединение закрыто.")
            break

if __name__ == "__main__":
    main()
```

**Вывод**
В результате был реализован многопользовательский чат на TCP.
Каждый клиент может отправлять сообщения, которые видят все подключённые пользователи.


## Задание 5. Веб-сервер с GET и POST

**Условие:**  
Реализовать простой веб-сервер для обработки GET и POST HTTP-запросов.

**Функционал:**  
- Принимать и записывать информацию о дисциплине и оценке.
- Отдавать HTML-страницу со списком всех дисциплин и оценок.

### Код сервера
```python
import socket
import threading
from urllib.parse import parse_qs

grades = {}

def generate_html():
    html = """
    <html>
    <head>
        <meta charset="utf-8">
        <title>Оценки</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f5f5f5;
                margin: 0;
                padding: 0;
            }
            .container {
                max-width: 600px;
                margin: 50px auto;
                background: #fff;
                padding: 20px 30px;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }
            h1, h2 { text-align: center; color: #333; }
            ul { list-style: none; padding: 0; }
            li {
                background: #e9f0ff;
                margin: 6px 0;
                padding: 10px 14px;
                border-radius: 8px;
                font-size: 16px;
            }
            form { margin-top: 20px; display: flex; flex-direction: column; gap: 10px; }
            input[type="text"] {
                padding: 10px;
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 8px;
            }
            input[type="submit"] {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                font-size: 14px;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                transition: 0.2s;
            }
            input[type="submit"]:hover { background-color: #45a049; }
            p { text-align: center; color: #777; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Список оценок</h1>
    """

    if grades:
        html += "<ul>"
        for subject, grade in grades.items():
            html += f"<li><b>{subject}</b>: {grade}</li>"
        html += "</ul>"
    else:
        html += "<p>Пока нет оценок.</p>"

    html += """
            <h2>Добавить оценку</h2>
            <form method="POST">
                <input type="text" name="subject" placeholder="Дисциплина">
                <input type="text" name="grade" placeholder="Оценка">
                <input type="submit" value="Сохранить">
            </form>
        </div>
    </body>
    </html>
    """
    return html

def handle_request(request_data):
    try:
        headers, body = request_data.split("\r\n\r\n", 1)
    except ValueError:
        headers, body = request_data, ""

    lines = headers.split("\r\n")
    method, path, _ = lines[0].split()

    if method == "POST":
        data = parse_qs(body)
        subject = data.get("subject", [""])[0].strip()
        grade = data.get("grade", [""])[0].strip()
        if subject and grade:
            grades[subject] = grade

    response_body = generate_html()
    response = "HTTP/1.1 200 OK\r\n"
    response += "Content-Type: text/html; charset=utf-8\r\n"
    response += f"Content-Length: {len(response_body.encode('utf-8'))}\r\n"
    response += "\r\n"
    response += response_body
    return response

def handle_client(client_socket, addr):
    try:
        request = client_socket.recv(1024).decode("utf-8", errors="ignore")
        if not request:
            client_socket.close()
            return

        headers = request.split("\r\n\r\n", 1)[0]
        content_length = 0
        for line in headers.split("\r\n"):
            if line.lower().startswith("content-length:"):
                content_length = int(line.split(":")[1].strip())

        body = request.split("\r\n\r\n", 1)[1] if "\r\n\r\n" in request else ""
        body_bytes = body.encode("utf-8")
        while len(body_bytes) < content_length:
            body_bytes += client_socket.recv(1024)
        full_request = headers + "\r\n\r\n" + body_bytes.decode("utf-8", errors="ignore")

        response = handle_request(full_request)
        client_socket.sendall(response.encode("utf-8"))
    finally:
        client_socket.close()

def run_server():
    host = "127.0.0.1"
    port = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Многопоточный сервер запущен на http://{host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Подключился клиент {addr}")
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    run_server()
```

**Вывод**
В результате был реализован многопоточный веб-сервер, который обрабатывает POST-запросы для добавления данных и GET-запросы для отображения списка оценок в виде HTML-страницы.

**Общий вывод**

В ходе лабораторной работы:

- реализованы клиент–серверные приложения на UDP и TCP;
- разработан многопоточный HTTP-сервер;
- создан многопользовательский чат с использованием потоков;
- реализован веб-сервер для работы с GET/POST-запросами.

Работа позволила закрепить навыки работы с сокетами и потоками в Python.