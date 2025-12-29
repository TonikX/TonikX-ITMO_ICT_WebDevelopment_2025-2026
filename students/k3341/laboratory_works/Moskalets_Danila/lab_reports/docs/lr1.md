# Лабораторная работа №1

**Студент:** Москалец Данила Алексеевич  
**Университет:** ИТМО  
**Группа:** К3341  

---

## Содержание

1. [Задание 1 (UDP)](#задание-1-udp)
2. [Задание 2 (TCP)](#задание-2-tcp)
3. [Задание 3 (HTTP)](#задание-3-http)
4. [Задание 4 (Многопользовательский чат)](#задание-4-многопользовательский-чат)
5. [Задание 5 (Web-сервер)](#задание-5-web-сервер)

---

## Задание 1 (UDP)<a id="задание-1-udp"></a>

### Условие
Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.

### Требования
- Использовать библиотеку `socket`.
- Реализовать обмен с помощью протокола UDP.

### Код:

server_udp.py:
```python
import socket

HOST = '127.0.0.1'
PORT = 9090

# создаем udp сокет: af_inet - ipv4, sock_dgram - udp
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# привязываем сокет к адресу
server_socket.bind((HOST, PORT))
print(f"UDP сервер запущен на {HOST}:{PORT}")

while True:
    # получаем сообщение от клиента
    data, addr = server_socket.recvfrom(1024)
    message = data.decode('utf-8')
    print(f"Получено сообщение от {addr}: {message}")

    # отправляем ответ клиенту
    response = "Hello, client"
    server_socket.sendto(response.encode('utf-8'), addr)
```

client_udp.py:
```python
import socket

HOST = '127.0.0.1'
PORT = 9090

# создаем udp сокет: af_inet - ipv4, sock_dgram - udp
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# привязываем сокет к адресу
server_socket.bind((HOST, PORT))
print(f"UDP сервер запущен на {HOST}:{PORT}")

while True:
    # получаем сообщение от клиента
    data, addr = server_socket.recvfrom(1024)
    message = data.decode('utf-8')
    print(f"Получено сообщение от {addr}: {message}")

    # отправляем ответ клиенту
    response = "Hello, client"
    server_socket.sendto(response.encode('utf-8'), addr)
```

### Суть работы 
- Разработан UDP-клиент и сервер, которые обмениваются сообщениями. Клиент отправляет сообщение серверу, сервер его принимает и отвечает обратно. Основная цель - показать работу протокола UDP и обмен данными без установления соединения.

### Скриншоты работы
![Задание 1 работает](imgs/lr1.1_1.png)

---

## Задание 2 (TCP) <a id="задание-2-tcp"></a>

### Условие
Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.  
Вариант 3 - поиск площади трапеции.
### Требования
- Использовать библиотеку `socket`.
- Реализовать обмен с помощью протокола TCP.

### Код:

server_tcp.py:
```python
import socket

HOST = '127.0.0.1'
PORT = 9090

# создаем tcp пакет: SOCK_STREAM - tcp
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)  # ждем подключения одного клиента

print(f"Сервер запущен на {HOST}:{PORT}")
conn, addr = server_socket.accept()  # ждем подключение
print(f"Подключен клиент: {addr}")

while True:
    data = conn.recv(1024).decode()  # получаем данные
    if not data:
        break
    try:
        a, b, h = map(float, data.split())
        area = ((a + b) / 2) * h
        conn.send(f"Площадь трапеции = {area}".encode())
    except:
        conn.send("Ошибка: введите три числа через пробел".encode())

conn.close()
server_socket.close()
```

client_tcp.py:
```python
import socket

HOST = '127.0.0.1'
PORT = 9090

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

while True:
    print("\nВведите стороны и высоту трапеции (a b h), или 'e' для выхода:")
    msg = input("> ")
    if msg.lower() == 'e':
        break

    client_socket.send(msg.encode())
    data = client_socket.recv(1024).decode()
    print("Ответ сервера:", data)

client_socket.close()
```

### Суть работы 
- Разработан TCP-клиент и сервер для вычисления площади трапеции. Клиент отправляет серверу три числа (длины оснований и высоту), сервер вычисляет площадь и возвращает результат.

### Скриншоты работы
![Задание 2 работает](imgs/lr1.2_1.png)

---

## Задание 3 (HTTP) <a id="задание-3-http"></a>

### Условие
Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла index.html.

### Требования
- Использовать библиотеку `socket`.

### Код:

index.html:
```html
<html>
<head>
    <meta charset="UTF-8">
    <title>Document</title>
</head>
<body>
    <h1>Hello world!</h1>
</body>
</html>
```

server_http.py:
```python
import socket

HOST = '127.0.0.1'
PORT = 9090

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"HTTP сервер запущен на http://{HOST}:{PORT}")

while True:
    conn, addr = server_socket.accept()
    print(f"Подключился клиент: {addr}")

    request = conn.recv(1024).decode('utf-8')
    print("Получен запрос:")
    print(request)

    # загружаем html из файла
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            body = f.read()

        # формируем http-ответ
        response = (
            "HTTP/1.1 200 OK\r\n" # код состояния 
            "Content-Type: text/html; charset=utf-8\r\n" # заголовки
            f"Content-Length: {len(body.encode('utf-8'))}\r\n" # заголовки
            "\r\n"
            f"{body}" # тело ответа
        )
    except FileNotFoundError:
        response = (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            "\r\n"
            "<h1>404 Файл не найден</h1>"
        )

    conn.sendall(response.encode('utf-8'))
    conn.close()
```

### Суть работы
Разработан HTTP-сервер на Python с использованием сокетов. Сервер принимает запросы от клиента, загружает HTML-файл index.html и возвращает его браузеру в виде HTTP-ответа.

### Скриншоты работы
![Задание 3 работает](imgs/lr1.3_1.png)
![Задание 3 работает](imgs/lr1.3_2.png)
---

## Задание 4 (Многопользовательский чат) <a id="задание-4-многопользовательский-чат"></a>

### Условие
Реализовать двухпользовательский или многопользовательский чат. Клиенты подключаются к серверу и обмениваются сообщениями через сервер.

### Требования
- Обязательно использовать библиотеку `socket`.
- Для многопользовательского чата использовать библиотеку `threading`.
- Протокол TCP — 100% баллов; UDP — 80% (для UDP использовать потоки для приёма сообщений).

### Код:

server_chat.py:
```python
import socket
import threading

HOST = '127.0.0.1'
PORT = 9090

clients = {}  # {client_socket: client_address}


# отправка сообщений всем клиентам кроме отправителя
def broadcast(message, sender_socket):
    for client in list(clients.keys()):
        if client != sender_socket:
            try:
                client.send(message)
            except:
                del clients[client]


# обработка сообщений от конкертного клиента
def handle_client(client_socket):
    print(f"+ Подключен {clients[client_socket]}")
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"({clients[client_socket][0]}:{clients[client_socket][1]}) {message}")
            broadcast(f"({clients[client_socket][0]}:{clients[client_socket][1]}): {message}".encode('utf-8'), client_socket)
        except:
            break
    print(f"- Отключен {clients[client_socket]}")
    del clients[client_socket]
    client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"HTTP сервер запущен на http://{HOST}:{PORT}")

    while True:
        client_socket, client_address = server.accept()
        clients[client_socket] = client_address
        thread = threading.Thread(target=handle_client, args=(client_socket, ))
        thread.start()


if __name__ == "__main__":
    start_server()
```

client_chat.py:
```python
import socket
import threading

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9090


# получение сообщения от сервера
def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if message:
                print("\n" + message)
        except:
            print("Отключено от сервера.")
            break


def client_main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_HOST, SERVER_PORT))
    print("Подключено к серверу. Можете писать сообщения:")

    # запускаем поток для получения сообщений
    thread = threading.Thread(target=receive_messages, args=(sock,))
    thread.start()

    # отправка сообщений
    while True:
        msg = input()
        if msg.lower() == 'exit':
            break
        sock.send(msg.encode('utf-8'))

    sock.close()


if __name__ == "__main__":
    client_main()
```

### Суть работы
Разработан многопользовательский чат на TCP с использованием потоков (threading). Сервер обрабатывает подключения нескольких клиентов одновременно, пересылая сообщения всем остальным пользователям. Клиент может одновременно получать и отправлять сообщения. 

### Скриншоты работы
![Задание 4 работает](imgs/lr1.4_1.png)
---

## Задание 5 (Web-сервер) <a id="задание-5-web-сервер"></a>

### Условие
Написать простой веб‑сервер на Python с использованием `socket`, который:
- принимает и записывает информацию о дисциплине и оценке (POST),
- возвращает HTML‑страницу со всеми оценками (GET).

### Требования
- Использовать библиотеку `socket`.

### Код:

server_http.py:
```python
import socket
import urllib.parse


class MyHTTPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.data = {}  # { "Математика": [5, 4], "Физика": [3] }

    # запуск сервера на сокете, обработка входящих соединений
    def serve_forever(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Сервер запущен на http://{self.host}:{self.port}")

        while True:
            client_socket, addr = server_socket.accept()
            self.serve_client(client_socket)
            client_socket.close()

    # обработка клиентского подключения
    def serve_client(self, client_socket):
        request = client_socket.recv(4096).decode('utf-8')
        if not request:
            return

        # первая строка: метод, путь, версия
        first_line = request.split('\r\n')[0]  # POST / HTTP/1.1
        method, path, _ = first_line.split()

        if method == 'POST':
            body = request.split('\r\n\r\n')[1]  # все, что после пустой строки - тело
            params = urllib.parse.parse_qs(body)  # превращаем в словарь тело http-запроса (subject=Математика&grade=5)
            subject = params.get('subject', [''])[0].strip()
            grade = params.get('grade', [''])[0]

            if subject and grade:
                self.data.setdefault(subject, []).append(grade)

            self.send_response(client_socket, "HTTP/1.1 303 See Other\r\nLocation: /\r\n\r\n")

        elif method == 'GET':
            html = self.generate_html()
            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=utf-8\r\n"
                f"Content-Length: {len(html.encode('utf-8'))}\r\n"
                "\r\n"
                f"{html}"
            )
            client_socket.sendall(response.encode('utf-8'))

    def generate_html(self):
        rows = ""
        for subj, grades in self.data.items():
            rows += f"<tr><td>{subj}</td><td>{', '.join(grades)}</td></tr>"
        return f"""
        <html>
        <head>
            <meta charset="utf-8">
            <title>Журнал оценок</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f6f8;
                    margin: 0;
                    padding: 20px;
                }}
                h1 {{
                    text-align: center;
                    color: #2c3e50;
                }}
                form {{
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    max-width: 400px;
                    margin: 20px auto;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                }}
                input[type="text"], input[type="number"] {{
                    width: 100%;
                    padding: 8px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    margin-top: 5px;
                    margin-bottom: 10px;
                }}
                input[type="submit"] {{
                    width: 100%;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 10px;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 16px;
                }}
                input[type="submit"]:hover {{
                    background-color: #45a049;
                }}
                table {{
                    margin: 30px auto;
                    border-collapse: collapse;
                    width: 80%;
                    background: white;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 10px;
                    text-align: center;
                }}
                th {{
                    background-color: #4CAF50;
                    color: white;
                }}
                tr:nth-child(even) {{
                    background-color: #f2f2f2;
                }}
            </style>
        </head>
        <body>
            <h1>Журнал оценок</h1>
            <form method="POST">
                <label>Дисциплина:</label>
                <input type="text" name="subject" required>
                <label>Оценка:</label>
                <input type="number" name="grade" min="1" max="5" required>
                <input type="submit" value="Добавить">
            </form>
            <table>
                <tr><th>Дисциплина</th><th>Оценки</th></tr>
                {rows}
            </table>
        </body>
        </html>
        """

    def send_response(self, client_socket, response_text):
        client_socket.sendall(response_text.encode('utf-8'))


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 9090
    server = MyHTTPServer(host, port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен.")
```

### Суть работы
Разработан простой веб-сервер на Python с обработкой GET и POST запросов. Сервер принимает данные о дисциплине и оценке, сохраняет их и возвращает HTML-страницу со списком всех оценок.

### Скриншоты работы
![Задание 5 работает](imgs/lr1.5_1.png)
---

## Вывод <a id="вывод"></a>
В ходе лабораторной работы №1 были изучены и реализованы различные сетевые приложения на Python с использованием библиотеки socket: обмен сообщениями по UDP, клиент-серверные вычисления по TCP, работа HTTP-сервера с HTML-страницами, многопользовательский чат и веб-сервер с обработкой GET и POST-запросов. Работа позволила закрепить практические навыки работы с протоколами UDP, TCP, потоками, HTTP и передачей данных между клиентом и сервером.