# Отчет по лабораторной работе №1

## Структура лабораторной работы

1. **UDP клиент-сервер**

   * `task1/client.py` — клиент, отправляющий сообщение серверу и получающий ответ.
   * `task1/server.py` — сервер, принимающий сообщения от клиента и отправляющий ответ.

2. **TCP клиент-сервер с решением квадратного уравнения**

   * `task2/client.py` — клиент, отправляющий коэффициенты серверу и получающий решение.
   * `task2/server.py` — сервер, принимающий коэффициенты, вычисляющий корни и отправляющий результат.

3. **HTTP сервер с отдачей HTML**

   * `task3/server.py` — простой HTTP сервер, отдающий статическую страницу `index.html`.
   * `task3/index.html` — HTML страница для теста.

4. **Многопользовательский чат на TCP**

   * `task4/client.py` — клиент для подключения к чату.
   * `task4/server.py` — сервер, поддерживающий многопользовательский чат с рассылкой сообщений.

5. **Минимальный HTTP сервер с обработкой POST**

   * `task5/server.py` — сервер для хранения и добавления оценок через веб-форму.

---

## Задание 1 — UDP клиент-сервер

**Описание:**
Клиент отправляет приветствие, сервер принимает его и отвечает.

**Код клиента (`task1/client.py`):**

```python
import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 12400

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message = f"Hello, Server! "
client_socket.sendto(message.encode(), (SERVER_HOST, SERVER_PORT))
print("Отправлено серверу: ", message)

data, addr = client_socket.recvfrom(1024)
print("Ответ от сервера: ", data.decode())
client_socket.close()
```

**Код сервера (`task1/server.py`):**

```python
import socket

Host = "127.0.0.1"
Port = 12400

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((Host, Port))
print(f"UDP-сервер запущен на {Host}:{Port}")

while True:
    data, addr = server_socket.recvfrom(1024)
    message = data.decode()
    print("Получено от", addr, ":", message)
    reply = "Hello client! "
    server_socket.sendto(reply.encode(), addr)
```

---

## Задание 2 — TCP клиент-сервер с решением квадратного уравнения

**Описание:**
Клиент отправляет коэффициенты `a, b, c`, сервер вычисляет корни уравнения `ax^2 + bx + c = 0` и отправляет результат.

**Код клиента (`task2/client.py`):**

```python
import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

print("Решение квадратного уравнения ax^2 + bx + c = 0")
a = float(input("Введите коэффициент a: "))
b = float(input("Введите коэффициент b: "))
c = float(input("Введите коэффициент c: "))

req = str(a) + "," + str(b) + "," + str(c)
client_socket.send(req.encode())

result = client_socket.recv(1024).decode()
print("Результат: ", result)
client_socket.close()
```

**Код сервера (`task2/server.py`):**

```python
import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print(f"TCP сервер запущен на {SERVER_HOST}:{SERVER_PORT}")

while True:
    client_socket, client_addr = server_socket.accept()
    print(f"Подключился клиент: {client_addr}")
    try:
        print("Начинаем обработку данных...")
        req = client_socket.recv(1024).decode()
        operands = req.split(",")
        a, b, c = float(operands[0]), float(operands[1]), float(operands[2])
        print(f"Получены коэффициенты: a = {a}, b = {b}, c = {c}")
    except ValueError:
        result = "Ошибка: неверный ввод коэффициентов."
        client_socket.send(result.encode())
        client_socket.close()
        continue

    discriminant = b**2 - 4 * a * c
    print(f"Дискриминант: {discriminant}")
    if discriminant > 0:
        root1 = (-b + discriminant**0.5) / (2 * a)
        root2 = (-b - discriminant**0.5) / (2 * a)
        result = f"Два корня: x1 = {root1}, x2 = {root2}"
    elif discriminant == 0:
        root = -b / (2 * a)
        result = f"Один корень: x = {root}"
    else:
        result = "Нет действительных корней."

    client_socket.send(result.encode())
    client_socket.close()
```

---

## Задание 3 — HTTP сервер с отдачей HTML

**Описание:**
Сервер отдает статическую страницу `index.html`.

**Код сервера (`task3/server.py`):**

```python
import socket

def handle_client(client_socket):
    request = client_socket.recv(1024).decode('utf-8')
    print(f"Request received:\n{request}")

    with open(r"C:\Users\Lenovo\Desktop\ITMO_2025\Web_Programming\First_lab\Thrid_task\index.html", 'r') as file:
        content = file.read()

    response = f"""HTTP/1.1 200 OK Content-Type: text/html {content}"""
    client_socket.sendall(response.encode('utf-8'))
    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(1)
    print("Server is listening on port 8080...")
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        handle_client(client_socket)

start_server()
```

**HTML (`task3/index.html`):**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My Simple Server</title>
</head>
<body>
    <h1>Hello from Python socket server!</h1>
    <p>This page is served by sockets, not Flask or Django.</p>
</body>
</html>
```

---

## Задание 4 — Многопользовательский чат на TCP

**Код клиента (`task4/client.py`):**

```python
import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message: print(message)
        except: break

def send_messages(client_socket):
    while True:
        try:
            message = input()
            if message.lower() == "exit":
                print("Disconnecting from server...")
                client_socket.close()
                break
            client_socket.send(message.encode('utf-8'))
        except: break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5555))
    print("Connected to server. Type messages and press Enter. Type 'exit' to quit.")
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()
    threading.Thread(target=send_messages, args=(client_socket,), daemon=True).start()
    while True:
        try:
            if client_socket.fileno() == -1: break
        except: break

start_client()
```

**Код сервера (`task4/server.py`):**

```python
import socket
import threading

clients = []
client_names = {}
client_count = 0
running = True

def broadcast(message, sender_socket=None):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except: continue

def handle_client(client_socket):
    name = client_names[client_socket]
    client_socket.settimeout(1.0)
    while running:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                full_message = f"{name}: {message}"
                print(full_message)
                broadcast(full_message, sender_socket=client_socket)
            else: break
        except socket.timeout: continue
        except: break
    if client_socket in clients: clients.remove(client_socket)
    if client_socket in client_names: del client_names[client_socket]
    client_socket.close()
    broadcast(f"{name} покинул чат.")
    print(f"{name} покинул чат.")

def start_server():
    global client_count, running
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5555))
    server_socket.listen(5)
    server_socket.settimeout(1.0)
    print("Сервер запущен и слушает порт 5555...")
    try:
        while running:
            try:
                client_socket, client_address = server_socket.accept()
            except socket.timeout: continue
            client_count += 1
            client_name = f"Client{client_count}"
            client_names[client_socket] = client_name
            clients.append(client_socket)
            print(f"{client_name} подключился с адреса {client_address}")
            threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()
    except KeyboardInterrupt:
        running = False
        for client in clients: client.close()
        server_socket.close()
        print("Сервер остановлен.")

if __name__ == "__main__":
    start_server()
```

---

## Задание 5 — Минимальный HTTP сервер с обработкой POST

**Код сервера (`task5/server.py`):**

```python
import socket
import threading
import urllib.parse

grades = {}

def generate_html():
    html = """<html><head><title>Grades</title></head><body>
<h1>Grades List</h1><table border="1"><tr><th>Subject</th><th>Grades</th></tr>"""
    for subject, grade_list in grades.items():
        grades_str = ", ".join(grade_list)
        html += f"<tr><td>{subject}</td><td>{grades_str}</td></tr>"
    html += """</table><br>
<form method="POST" action="/">
<input type="text" name="subject" placeholder="Subject" required><br>
<input type="text" name="grade" placeholder="Grade" required><br>
<input type="submit" value="Add Grade"></form></body></html>"""
    return html

def handle_request(client_socket):
    request = client_socket.recv(1024).decode('utf-8')
    print(f"Received request:\n{request}")
    if not request: client_socket.close(); return
    lines = request.split("\r\n")
    method, path, _ = lines[0].split()
    if method == "POST":
        body = request.split("\r\n\r\n", 1)[1]
        params = urllib.parse.parse_qs(body)
        subject = params.get("subject", [""])[0].strip()
        grade = params.get("grade", [""])[0].strip()
        if subject and grade:
            grades.setdefault(subject, []).append(grade)
    html_content = generate_html()
    response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + html_content
    client_socket.sendall(response.encode("utf-8"))
    client_socket.close()

def start_server(host="localhost", port=8080):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server started at http://{host}:{port}")
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        threading.Thread(target=handle_request, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()
```

---

### Выводы

* Реализованы различные типы сетевых взаимодействий: UDP, TCP, HTTP.
* Получен опыт работы с сокетами, многопоточностью и обработкой HTTP-запросов.
* Все задания структурированы по папкам и снабжены комментариями.
