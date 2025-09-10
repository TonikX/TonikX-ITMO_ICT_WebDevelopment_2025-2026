# Лабораторная работа №1

## Задание 1
Реализован клиент-серверный чат с использованием протокола UDP. Клиент отправляет сообщение "Hello, server" серверу, который отображает его в консоли и отправляет ответ "Hello, client", который отображается у клиента.

**Реализация:**
- Клиент создает UDP-сокет и отправляет сообщение серверу по адресу localhost:8081
- Сервер создает UDP-сокет, привязывается к адресу localhost:8081 и ожидает сообщения
- При получении сообщения сервер выводит его в консоль и отправляет ответ клиенту

**Пример кода:**

*client.py:*
```python
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client_socket.sendto(b'Hello, server!', ("localhost", 8081))

response, address = client_socket.recvfrom(1024)
print(response.decode())
```

*server.py:*
```python
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('localhost', 8081))

while True:
    data, address = server_socket.recvfrom(1024)
    print(data.decode())

    response = 'Hello, client!'
    server_socket.sendto(response.encode(), address)
```
## Задание 2
Реализован клиент-серверный калькулятор с использованием протокола TCP. Клиент отправляет параметры для математической операции, сервер обрабатывает данные и возвращает результат.

**Реализация:**
- Клиент создает TCP-сокет и подключается к серверу по адресу localhost:8082
- Клиент отправляет строку с параметрами, разделенными запятыми
- Сервер принимает подключение, получает данные и передает их в функцию математической обработки
- В данном случае реализована операция умножения двух чисел (по варианту студента)
- Результат отправляется клиенту

**Пример кода:**

*client.py:*
```python
import socket

while True:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        user_input = str(input())
        client_socket.connect(('localhost', 8082))
        client_socket.sendall(user_input.encode())
        response = client_socket.recv(1024)
        print(response.decode())
    except Exception as e:
        print(f"wrong input: {e}")
        continue

    client_socket.close()
```

*server.py:*
```python
import socket
from mathematics import parse_math

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('localhost', 8082))
server_socket.listen(1)

while True:
    client_connection, client_address = server_socket.accept()
    request = client_connection.recv(1024).decode()

    math = parse_math(request).do_math()

    client_connection.sendall(str(math).encode())
```

*mathematics.py:*
```python
import dataclasses

@dataclasses.dataclass
class Math:
    a: int
    b: int
    h: int

    def do_math(self) -> float:
        return (self.a + self.b) / self.h

def parse_math(string: str) -> Math:
    split_string = string.split(",")
    return Math(int(split_string[0]), int(split_string[1]), int(split_string[2]))

def decode_math(math: Math) -> str:
    return f"{math.a},{math.b},{math.h}"
```
## Задание 3
Реализован простой HTTP-сервер, который при подключении клиента отправляет содержимое HTML-файла.

**Реализация:**
- Сервер создает TCP-сокет и привязывается к адресу localhost:8001
- При подключении клиента сервер читает содержимое файла index.html и отправляет его клиенту
- Клиент подключается к серверу и выводит полученный HTML-код в консоль

**Пример кода:**

*client.py:*
```python
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("localhost", 8001))
    print(s.recv(1024).decode())
```

*server.py:*
```python
import socket

with open("index.html", "rb") as f:
    html = f.read()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    host = 'localhost'
    port = 8001

    s.bind((host, port))
    s.listen()

    while True:
        con, addr = s.accept()
        with con:
            con.sendall(html)
```

*index.html:*
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Ого это же сайт</title>
</head>
<body>
    <h1>Неужели это сайт? Да это сайт</h1>
</body>
</html>
```
## Задание 4
Реализован многопользовательский чат с использованием TCP и потоков.

**Реализация:**
- Сервер использует threading для обработки каждого клиента в отдельном потоке
- Каждый клиент при подключении отправляет свой уникальный ID серверу
- Сервер хранит подключения всех клиентов в словаре
- При получении сообщения от клиента, сервер рассылает его всем подключенным клиентам
- Клиент использует два потока: один для отправки сообщений, другой для приема сообщений
- Сообщения передаются в формате JSON с указанием ID отправителя

**Пример кода:**

*client.py:*
```python
import socket
import json
import threading

user_id = input()

def get_data(s):
    while True:
        data = s.recv(1024).decode()
        msg = json.loads(data)
        if msg['id'] != user_id:
            print(data)

def send_data(s):
    while True:
        msg = input()
        if msg:
            s.sendall(msg.encode())

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 8082))
    s.sendall(user_id.encode())
    threading.Thread(target=get_data, args=[s]).start()
    threading.Thread(target=send_data, args=[s]).start()

if __name__ == '__main__':
    main()
```

*server.py:*
```python
import socket
import threading
from chat.message_entity import Message

clients = {}

def new_client(conn):
    client_id = get_client_id(conn)
    print("New client id:", client_id)

    clients[client_id] = conn
    while True:
        message = conn.recv(1024).decode()
        if message:
            print("message received:", message)
            send_to_all(Message(client_id, message))

def get_client_id(conn) -> str:
    while True:
        client_id = conn.recv(1024).decode()
        print("Client id:", client_id)
        if client_id not in clients:
            clients[client_id] = conn
            break
        elif client_id in clients:
            print("wrong id", client_id)
            conn.send(b"id used")
    print("correct id", client_id)
    return client_id

def send_to_all(message: Message):
    msg = '{' + f'"id": "{message.id}", "msg": "{message.msg}"' + '}'
    for i in clients.keys():
        conn = clients[i]
        print(f"sending message to {i}:", msg)
        conn.sendall(msg.encode())

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 8082))
        s.listen()
        while True:
            conn, addr = s.accept()
            threading.Thread(target=new_client, args=[conn]).start()

if __name__ == '__main__':
    main()
```

*chat/message_entity.py:*
```python
from dataclasses import dataclass

@dataclass
class Message:
    id: str
    msg: str
```
## Задание 5
Реализован веб-сервер для обработки GET и POST HTTP-запросов.

**Реализация:**
- Сервер обрабатывает GET-запросы по адресу /grades для отображения оценок
- Сервер обрабатывает POST-запросы по адресу /grades для добавления оценок
- Данные хранятся в памяти сервера в виде словаря
- Для POST-запросов данные передаются в формате JSON с полями lesson и grade
- Для GET-запросов сервер возвращает HTML-страницу со списком всех оценок
- Реализованы классы Request и Response для обработки HTTP-запросов и ответов
- Реализована обработка заголовков и содержимого запросов

**Пример кода:**

*webserver.py:*
```python
import socket

from lesson import *
from request import *

class MyHTTPServer:
    # Параметры сервера
    def __init__(self, host, port, server_name):
        self._host = host
        self._port = port
        self._server_name = server_name
        self.lessons = Lessons()

    def serve_forever(self):
        # 1. Запуск сервера на сокете, обработка входящих соединений
        serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)

        try:
            serv_sock.bind((self._host, self._port))
            serv_sock.listen()

            while True:
                conn, _ = serv_sock.accept()
                try:
                    self.serve_client(conn)
                except Exception as e:
                    print('Client serving failed', e)
        finally:
            serv_sock.close()

    def serve_client(self, conn):
        # 2. Обработка клиентского подключения
        try:
            req = self.parse_request(conn)
            resp = self.handle_request(req)
            self.send_response(conn, resp)
        except ConnectionResetError:
            conn = None
        except Exception as e:
            print('Client serving failed', e)

        if conn:
            conn.close()

    def parse_request(self, conn) -> Request:
        # 3. функция для обработки заголовка http+запроса.
        # Python, сокет предоставляет возможность создать вокруг него некоторую обертку,
        # которая предоставляет file object интерфейс. Это дайте возможность построчно обработать запрос.
        # Заголовок всегда - первая строка. Первую строку нужно разбить на 3 элемента  (метод + url + версия протокола).
        # URL необходимо разбить на адрес и параметры
        # (isu.ifmo.ru/pls/apex/f?p=2143 , где isu.ifmo.ru/pls/apex/f, а p=2143 - параметр p со значением 2143)
        buffer = b''
        while b'\r\n' not in buffer:
            buffer += conn.recv(1)
        buffer = buffer.decode().split(" ")

        headers = self.parse_headers(conn)
        content = self.parse_content(conn, headers)
        url_params = buffer[1].split("?")
        if len(url_params) == 1:
            url_params_dict = {}
        else:
            url_params_dict = {}

            for i in url_params[1].split("&"):
                i = i.split("=")
                url_params_dict[i[0]] = i[1]

        return Request(buffer[0], buffer[1].split("?")[0], buffer[2], url_params_dict, headers, content)

    @staticmethod
    def parse_headers(conn) -> Dict[str, str]:
        # 4. Функция для обработки headers.
        # Необходимо прочитать все заголовки после первой строки до появления пустой строки и сохранить их в массив.
        headers = {}

        while True:
            buffer = b''
            while b'\r\n' not in buffer:
                buffer += conn.recv(1)
            line = buffer.decode().split(": ")
            if line[0] == '\r\n':
                break
            headers[line[0].lower()] = line[1]

        return headers

    def handle_request(self, req: Request) -> Response:
        # 5. Функция для обработки url в соответствии с нужным методом.
        # В случае данной работы, нужно будет создать набор условий, который обрабатывает GET или POST запрос.
        # GET запрос должен возвращать данные. POST запрос должен записывать данные на основе переданных параметров.
        if req.method == "GET" and req.url == "/grades":
            return parse_get_grades_req(self.lessons, req)
        elif req.method == "POST" and req.url == "/grades":
            return parse_set_grades_req(self.lessons, req)
        else:
            return Response(404, "Not Found")

    @staticmethod
    def parse_content(conn, headers) -> Optional[str]:
        if "content-length" not in headers.keys():
            return None

        output = conn.recv(int(headers['content-length']))
        return output.decode()

    @staticmethod
    def send_response(conn, resp: Response):
        # 6. Функция для отправки ответа. Необходимо записать в соединение status line вида HTTP/1.1 <status_code> <reason>.
        # Затем, построчно записать заголовки и пустую строку, обозначающую конец секции заголовков.
        output = f"{resp.http_version} {resp.status} {resp.reason}\r\n\r\n{resp.body}"
        wfile = conn.makefile('wb')
        wfile.write(output.encode())

if __name__ == '__main__':
    host = "localhost"
    port = 8081
    name = 'name'
    serv = MyHTTPServer(host, port, name)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        pass
```

*request.py:*
```python
from dataclasses import dataclass

from typing_extensions import Dict, Optional

@dataclass
class Request:
    method: str
    url: str
    http_version: str
    params: dict
    headers: Dict[str, str]
    content: Optional[str]

@dataclass
class Response:
    status: int
    reason: str
    http_version: str = 'HTTP/1.1'
    body: str = ''
```

*lesson.py:*
```python
import json

from request import *

class Lessons:

    def __init__(self):
        self.lessons = {}

    def set_grade(self, lesson: str, grade: int):
        self.lessons[lesson] = grade

    def get_grades_html(self) -> str:
        if len(self.lessons.keys()) == 0:
            return f'<h1>Пусто тута</h1>'
        out = ''
        for i in self.lessons.keys():
            out += f'<br>{i}: {self.lessons[i]}</br>'
        return out

def parse_set_grades_req(lessons: Lessons, req: Request) -> Response:
    if req.content is None or len(req.content) == 0:
        return Response(400, "empty content")

    try:
        json_data = json.loads(req.content)
        lessons.set_grade(json_data['lesson'], int(json_data['grade']))
    except json.decoder.JSONDecodeError:
        return Response(400, "invalid json")
    except KeyError:
        return Response(400, "invalid json")
    except ValueError:
        return Response(400, "invalid json")

    return Response(200, "OK")

def parse_get_grades_req(lessons: Lessons, req: Request) -> Response:
    return Response(200, "OK", body=lessons.get_grades_html())
```

## Вывод

В ходе выполнения лабораторной работы были реализованы различные сетевые приложения с использованием сокетов в Python. Были рассмотрены различные протоколы (UDP, TCP) и архитектуры (клиент-сервер, многопользовательский чат, HTTP-сервер):

- В первой задаче был реализован простой клиент-серверный чат с использованием UDP. Это позволило понять основы работы с UDP-сокетами и принципы обмена сообщениями между клиентом и сервером.

- Во второй задаче был создан клиент-серверный калькулятор с использованием TCP. Это позволило изучить работу с TCP-сокетами, обработку ошибок и передачу данных в формате строки.

- Третья задача была посвящена созданию простого HTTP-сервера, который отдает HTML-файл. Это помогло понять основы работы веб-серверов и протокола HTTP.

- В четвертой задаче нужно было сделать многопользовательский чат с использованием потоков. Это позволило изучить многопоточность в Python и создание более сложных сетевых приложений.

- А в пятой задаче - полноценный веб-сервер для обработки GET и POST запросов. Это позволило глубже понять структуру HTTP-запросов и ответов, а также работу с заголовками и содержимым запросов.

- В целом, лабораторная работа помогла получить практические навыки работы с сетевыми сокетами, понять различия между протоколами UDP и TCP, а также изучить основы веб-программирования.
