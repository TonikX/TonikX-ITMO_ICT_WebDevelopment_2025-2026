# Отчет по лабораторной работе №1
Выполнил Скобликов Кирилл, K3339

## Задание 1

Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.

Требования:
 - Обязательно использовать библиотеку socket.
 - Реализовать с помощью протокола UDP.

### Выполнение:
Клиент:
```python
import socket

# Создаем сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 8911)

# Отправляем сообщение серверу
client_socket.sendto(b'Hello, server', server_address)

# Получаем ответ от сервера (с адресом отправителя)
response, server_addr = client_socket.recvfrom(1024)
print(f'Ответ от сервера {server_addr}: {response.decode()}')

# Закрываем соединение
client_socket.close()
```

Сервер:
```python
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_socket.bind(('localhost', 8911))
print("UDP-сервер запущен на порту 8911...")

while True:
    client_connection, client_address = server_socket.recvfrom(1024)
    print(f'Подключение от {client_address}')
    request = client_connection.decode()
    print(f'Запрос от клиента: {request}')
    response = 'Hello, client'
    server_socket.sendto(response.encode(), client_address)
```

## Задание 2
Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

Варианты операций:

1. Теорема Пифагора.
2. Решение квадратного уравнения.
3. Поиск площади трапеции.
4. Поиск площади параллелограмма.

Порядок выбора варианта: Выбирается по порядковому номеру в журнале (пятый студент получает вариант 1 и т.д.).

Требования:
- Обязательно использовать библиотеку socket.
- Реализовать с помощью протокола TCP.

### Выполнение 
Сервер
```python
import socket
from math import sqrt

def quadratic_Solution(a, b, c):
    if a == 0:
        if b == 0:
            return "Уравнение вырождено"
        return round(-c / b, 2)

    D = b ** 2 - 4 * a * c

    if D < 0:
        return "Действительных корней нет"
    elif D == 0:
        root = float(-b / (2 * a))
        return round(root, 2)
    else:
        first_root = (-b - sqrt(D)) / (2 * a)
        second_root = (-b + sqrt(D)) / (2 * a)
        return round(first_root, 2), round(second_root, 2)


# Создаем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет к адресу и порту
server_socket.bind(('localhost', 8911))

# Начинаем слушать входящие подключения (ожидание клиентов)
server_socket.listen(1)
print("Сервер запущен на порту 8911...")

while True:
    # Принимаем соединение от клиента
    client_connection, client_address = server_socket.accept()
    print(f'Подключение от {client_address}')

    client_connection.sendall('Чтобы я мог решить квадратное уравнение, передай мне коэффициенты a, b и c в формате "a, b, c"'.encode())

    # Получаем сообщение от клиента
    while True:
        try:
            data = client_connection.recv(1024).decode()
            if not data:
                print(f"Клиент {client_address} отключился")
                break

            request = list(map(float, data.split(sep=', ')))
            response = quadratic_Solution(float(request[0]), float(request[1]), float(request[2]))
            if type(response) == tuple:
                client_connection.sendall(f'Первый корень: {response[0]}, Второй: {response[1]}'.encode())
            elif type(response) == float:
                client_connection.sendall(f'Единственный корень: {response}'.encode())
            else:
                client_connection.sendall(f'Либо отсутствуют действительные корни, либо уравнение вырождено'.encode())
        except:
            client_connection.sendall(f'Некорректные входные данные'.encode())

    # Закрываем соединение
    client_connection.close()
```

Клиент:
```python
import socket

# Создаем сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Подключаемся к серверу
client_socket.connect(('localhost', 8911))
print("Подключение к серверу установлено")

first_response = client_socket.recv(1024)
print(first_response.decode())

while True:
    ans = input("Введите коэффициенты (или 'exit' для выхода): ")

    if ans.lower() == 'exit':
        print("Завершение работы...")
        break

    client_socket.sendall(ans.encode())

    # Получаем ответ от сервера
    response = client_socket.recv(1024).decode()
    print(f'Ответ от сервера: {response}')

client_socket.close()
```

## Задание 3
Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла index.html.

Требования:
- Обязательно использовать библиотеку socket.

### Выполнение 
Сервер:
```python
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет к адресу и порту
server_socket.bind(('localhost', 8911))

# Начинаем слушать входящие подключения (ожидание клиентов)
server_socket.listen(1)
print("Сервер запущен на порту 8911...")

with open('index.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

while True:
    # Принимаем соединение от клиента
    client_connection, client_address = server_socket.accept()
    print(f'Подключение от {client_address}')

    # Получаем запрос от клиента (например, из браузера)
    request = client_connection.recv(1024).decode()
    print(f'Запрос клиента:\n{request}')

    # Формируем HTTP-ответ с заголовками и HTML-контентом
    http_response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=UTF-8\r\n"
        f"Content-Length: {len(html_content)}\r\n"
        "Connection: close\r\n"
        "\r\n"
        + html_content
    )

    # Отправляем HTTP-ответ клиенту
    client_connection.sendall(http_response.encode())

    # Закрываем соединение
    client_connection.close()
```

## Задание 4
Реализовать двухпользовательский или многопользовательский чат. Для максимального количества баллов реализуйте многопользовательский чат.

Требования:

- Обязательно использовать библиотеку socket.
- Для многопользовательского чата необходимо использовать библиотеку threading.

Реализация:

- Протокол TCP: 100% баллов.
- Протокол UDP: 80% баллов.
- Для UDP используйте threading для получения сообщений на клиенте.
- Для TCP запустите клиентские подключения и обработку сообщений от всех пользователей в потоках. Не забудьте сохранять пользователей, чтобы отправлять им сообщения.

### Выполнение:
Сервер:
```python
import socket
import threading


class ChatServer:
    def __init__(self, host='localhost', port=8911):
        self.host = host
        self.port = port
        self.socket = None
        self.clients = {}
        self.lock = threading.Lock()
        self.guest_counter = 0
        self.is_running = False
        self.admin_thread = None

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        self.is_running = True

        self.admin_thread = threading.Thread(target=self.admin_loop, daemon=True)
        self.admin_thread.start()

        print(f"Сервер запущен на {self.host}:{self.port}")
        print("Административные команды:")
        print("  /server_off - остановить сервер")

        try:
            while self.is_running:
                try:
                    self.socket.settimeout(1.0)
                    client_socket, addr = self.socket.accept()

                    if not self.is_running:
                        client_socket.close()
                        break

                    print(f"Новое подключение: {addr}")
                    guest_name = f"Гость {self.guest_counter}"
                    self.guest_counter += 1

                    with self.lock:
                        self.clients[client_socket] = guest_name

                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, guest_name)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                except socket.timeout:
                    continue
                except OSError as e:
                    if self.is_running:
                        print(f"Ошибка сокета: {e}")
                    break
        except KeyboardInterrupt:
            print("Получен сигнал прерывания")
            self.stop()
        finally:
            if self.is_running:  # Если еще не остановлен
                self.stop()

    def handle_client(self, client_socket, username):
        self.broadcast(f"{username} присоединился к чату!", exclude=client_socket)
        client_socket.send(f"Добро пожаловать, {username}!".encode())

        while self.is_running:
            try:
                client_socket.settimeout(1.0)
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                if self.is_running:
                    self.broadcast(f"{username}: {message}", exclude=client_socket)
            except:
                break

        self.remove_client(client_socket, username)

    def broadcast(self, message, exclude=None):
        with self.lock:
            disconnected = []
            for client, username in self.clients.items():
                if client != exclude:
                    try:
                        client.send(message.encode())
                    except:
                        disconnected.append(client)

            for client in disconnected:
                if client in self.clients:
                    del self.clients[client]

    def remove_client(self, client_socket, username):
        with self.lock:
            if client_socket in self.clients:
                del self.clients[client_socket]
        if self.is_running:
            self.broadcast(f"{username} покинул чат!")

        client_socket.close()
        print(f"Клиент {username} отключен")

    def admin_loop(self):
        while self.is_running:
            command = input()
            if command == '/server_off':
                print("Остановка сервера...")
                self.stop()
                break

    def stop(self):
        self.is_running = False
        with self.lock:
            for client in list(self.clients.keys()):
                client.close()

            self.clients.clear()

        if self.socket:
            self.socket.close()
            self.socket = None

        print("Сервер остановлен")


if __name__ == "__main__":
    server = ChatServer()
    server.start()
```

Клиент:
```python
import socket
import threading


class ChatClient:
    def __init__(self, host='localhost', port=8911):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = False

    def start(self):
        try:
            self.socket.connect((self.host, self.port))
            self.running = True
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()

            print("Подключение к чату установлено. Для выхода введите /quit")
            while self.running:
                message = input()
                if message == '/quit':
                    break
                self.socket.send(message.encode())
        except Exception as e:
            print(f"Ошибка подключения: {e}")
        finally:
            self.stop()

    def receive_messages(self):
        while self.running:
            try:
                message = self.socket.recv(1024).decode()
                if not message:
                    break
                print(message)
            except:
                break

    def stop(self):
        self.running = False
        self.socket.close()
        print("Отключение от чата")


if __name__ == "__main__":
    client = ChatClient()
    client.start()
```

## Задание 5
Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python.

Задание:

- Сервер должен:
  - Принять и записать информацию о дисциплине и оценке по дисциплине.
  - Отдать информацию обо всех оценках по дисциплинам в виде HTML-страницы.

### Выполнение:

```python
import socket
import urllib.parse
from collections import defaultdict

grades = []


def build_html():
    grouped = defaultdict(list)
    for d, g in grades:
        grouped[d].append(g)

    rows = ""
    for discipline, marks in grouped.items():
        marks_str = ", ".join(marks)
        rows += f"<tr><td>{discipline}</td><td>{marks_str}</td></tr>"

    html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>Оценки по дисциплинам</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f0f2f5;
                height: 100vh;
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            .container {{
                background-color: white;
                border-radius: 16px;
                padding: 30px 40px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                width: 450px;
                text-align: center;
            }}
            h1 {{
                margin-bottom: 20px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }}
            th, td {{
                border: 1px solid #ccc;
                padding: 8px;
            }}
            th {{
                background-color: #f7f7f7;
            }}
            input[type="text"] {{
                width: 90%;
                padding: 6px;
                margin: 5px 0;
                border: 1px solid #ccc;
                border-radius: 6px;
            }}
            input[type="submit"] {{
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 18px;
                border-radius: 6px;
                cursor: pointer;
                margin-top: 10px;
            }}
            input[type="submit"]:hover {{
                background-color: #45a049;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Список оценок</h1>
            <table>
                <tr><th>Дисциплина</th><th>Оценки</th></tr>
                {rows if rows else "<tr><td colspan='2'>Нет данных</td></tr>"}
            </table>

            <h2>Добавить новую оценку</h2>
            <form method="POST" action="/">
                <input type="text" name="discipline" placeholder="Дисциплина" required><br>
                <input type="text" name="grade" placeholder="Оценка" required><br>
                <input type="submit" value="Добавить">
            </form>
        </div>
    </body>
    </html>
    """
    return html


def read_http_request(conn):
    data = b""
    while b"\r\n\r\n" not in data:
        part = conn.recv(1024)
        if not part:
            break
        data += part

    header_part, _, body = data.partition(b"\r\n\r\n")
    headers = header_part.decode("utf-8", errors="ignore")

    content_length = 0
    for line in headers.split("\r\n"):
        if line.lower().startswith("content-length:"):
            try:
                content_length = int(line.split(":")[1].strip())
            except ValueError:
                content_length = 0
            break

    while len(body) < content_length:
        part = conn.recv(1024)
        if not part:
            break
        body += part

    full_request = header_part + b"\r\n\r\n" + body
    return full_request.decode("utf-8", errors="ignore")


def handle_request(request):
    headers, _, body = request.partition("\r\n\r\n")
    if not headers:
        return "HTTP/1.1 400 Bad Request\r\n\r\n"

    first_line = headers.split("\r\n")[0]
    try:
        method, path, _ = first_line.split()
    except ValueError:
        return "HTTP/1.1 400 Bad Request\r\n\r\n"

    if method == "POST":
        decoded_body = urllib.parse.unquote_plus(body)
        params = urllib.parse.parse_qs(decoded_body)
        discipline = params.get("discipline", [""])[0]
        grade = params.get("grade", [""])[0]

        if discipline and grade:
            grades.append((discipline, grade))

        return "HTTP/1.1 303 See Other\r\nLocation: /\r\n\r\n"

    html = build_html()
    return "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n" + html


def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('127.0.0.1', 8911))
        s.listen(5)
        print(f"Сервер запущен: http://{'127.0.0.1'}:{8911}/")

        while True:
            conn, addr = s.accept()
            with conn:
                request = read_http_request(conn)
                if not request:
                    continue
                response = handle_request(request)
                conn.sendall(response.encode("utf-8"))


if __name__ == "__main__":
    run_server()
```