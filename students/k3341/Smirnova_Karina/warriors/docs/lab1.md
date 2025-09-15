# Отчет по лабораторной работе №1

## Задание 1

Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно
отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно
отобразиться у клиента.

**Требования:**

* Обязательно использовать библиотеку socket.
* Реализовать с помощью протокола UDP.

### Реализация

**Сервер:**

```python
import socket

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Создали сокет UDP
socket.bind(('', 9090))  # Соединили сокет с хостом '' и портом 9090
socket.settimeout(60)

try:
    while True:

        try:
            data, addr = socket.recvfrom(1024)  # Чтение данных от клиента
            print(data.decode("utf-8"))  # Печатаем декодированные данные
            socket.sendto("Hi, client".encode("utf-8"), addr)  # Отправляем ответ на адрес отправителя

        except socket.timeout:
            print("Socket timeout")
            break

        except Exception as e:
            print("Exception: ", e)
            continue

except Exception as e:
    print("Exception: ", e)
finally:
    socket.close()
```

**Клиент:**

```python
import socket

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    socket.sendto("Hi, server".encode("utf-8"), ('localhost', 9090))

    data, server = socket.recvfrom(1024)
    print(data.decode("utf-8"))

except Exception as e:
    print("Exception: ", e)

finally:
    socket.close()
```

**Пояснения:**

Открываем UDP сокет **сервера** на localhost и порту 9090, после чего в бесконечном цикле пытаемся прочитать данные от
клиента и напечатать их, раскодировав. После чего отправляем сообщение обратно клиенту.

**Клиент** же также создает UDP сокет и без установки соединения, отправляет данные на localhost порт 9090. После чего
читает ответ сервера.

## Задание 2

Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры
которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

**Требования:**

* Обязательно использовать библиотеку socket.
* Реализовать с помощью протокола TCP.

### Реализация

**Сервер:**

```python
import socket
import math

def solvePifagor(a, b):
    return math.sqrt(a**2 + b**2)

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Создаем TCP сокет на localhost и порт 9090
socket.bind(('', 9090))
socket.settimeout(60)
socket.listen(3)

try:
    while True:
        clSocket, addr = socket.accept()  # Принимаем соединение

        try:
            data = clSocket.recv(1024).decode("utf-8")
            a, b = map(int, data.split(" "))
            res = solvePifagor(a, b)
            clSocket.send(str(res).encode("utf-8"))

        except Exception as e:
            clSocket.send(("Exception: " + str(e)).encode("utf-8"))

        finally:
            clSocket.close()

except Exception as e:
    print("Exception: ", e)

finally:
    socket.close()
```

**Клиент:**

```python
import socket

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Создаем TCP сокет на localhost и порт 9090

try:
    socket.connect(('localhost', 9090))  # Устанавливаем связь с сервером

    print("Введите 2 стороны прямоугольника через пробел")  # Получение данных с консоли
    try:
        data = str(input())
        socket.send(data.encode("utf-8"))

        result = socket.recv(1024).decode("utf-8")
        print("Результат = ", result)

    except Exception as e:
        print("Exception: ", e)

except Exception as e:
    print("Exception: ", e)

finally:
    socket.close()
```

**Пояснения:**

На **сервере** создаем функцию для выполнения математической операции. После Открываем TCP сокет сервера на localhost и 
порту 9090, после чего в бесконечном цикле принимаем соединение и пытаемся прочитать данные от
клиента и выполнить математическую операцию. Если данные успешно получены, раскодированы и вычислен результат, то
отправляем клиенту результат, иначе текст ошибки.

**Клиент** также создает TCP сокет и пытается установить соединение с сервером на localhost порт 9090. Если это прошло
успешно, то он запрашивает данные от клиента с консоли, отправляет их серверу, получает ответ и выводит его в консоль.

## Задание 3

Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее
HTML-страницу, которая сервер подгружает из файла index.html.

**Требования:**

* Обязательно использовать библиотеку socket.

### Реализация

**Сервер:**

```python
import socket
from datetime import datetime

def readPage(fileName="index.html"):
    try:
        with open(fileName, 'r', encoding="utf-8") as file:
            return file.read()

    except Exception as e:
        return f'<h1>Server Error: {e}</h1>'

def makeResponse(text):
    response = f"""
    HTTP/1.1 200 OK
    Date: {datetime.now()}
    Server: localhost
    Content-type:text/html; charset=UTF-8
    Content-Length: {len(text.encode("utf-8"))}
    
    {text} 
    """
    return response

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Создание TCP сокета
serverSocket.bind(('', 9090))
serverSocket.listen(3)
serverSocket.settimeout(60)

try:
    while True:
        clSocket, addr = serverSocket.accept()  # Устанавливаем соединение с клиентом

        try:
            request = clSocket.recv(1024).decode("utf-8")  # Читаем HTTP-запрос

            htmlText = readPage()  # Читаем страницу HTML

            http_response = makeResponce(htmlText)  # Формируем ответ

            clSocket.send(http_response.encode('utf-8'))  # Отправляем ответ

        except Exception as e:
            print("Exception: ", e)
            clSocket.send(f"""
            HTTP/1.1 500
            Error: {e} 
            """.encode('utf-8'))

        finally:
            clSocket.close()

except Exception as e:
    print("Exception: ", e)

finally:
    serverSocket.close()
```

**Клиент:**

```python
import socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    clientSocket.connect(('localhost', 9090))  # Устанавливаем связь с сервером

    http_request = """
    GET /index.html HTTP/1.1
    HOST: localhost 9090
    """

    clientSocket.send(http_request.encode('utf-8'))  # Отправляем запрос

    # Собираем ответ
    response = ''
    while True:
        part = clientSocket.recv(1024).decode('utf-8')
        if not part: break
        response += part

    print("Response:\n", response)

except Exception as e:
    print("Exception: ", e)

finally:
    clientSocket.close()
```

**index.html**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1>Index page</h1>
</body>
</html>
```

**Пояснения:**

Для **сервера** создаем TCP сокет на localhost 9090, устанавливаем соединение с клиентом с помощью метода accept. Читаем 
файл index.html с помощью метода readPage(), формируем ответ для клиента с помощью метода makeResponse() и отправляем
его клиенту.

На стороне **клиента** создаем TCP сокет и пытается установить соединение с сервером на localhost порт 9090. Если это прошло
успешно, то он отправляет HTTP GET запрос серверу на получение страницы index.html, получает ответ от сервера и 
печатает.

## Задание 4

Реализовать двухпользовательский или многопользовательский чат. Для максимального количества баллов реализуйте 
многопользовательский чат.

**Требования:**

* Обязательно использовать библиотеку socket.
* Для многопользовательского чата необходимо использовать библиотеку threading.
* Протокол TCP: 100% баллов.
* Протокол UDP: 80% баллов.
* Для UDP используйте threading для получения сообщений на клиенте.
* Для TCP запустите клиентские подключения и обработку сообщений от всех пользователей в потоках. Не забудьте сохранять
пользователей, чтобы отправлять им сообщения.

### Реализация

**Сервер:**

```python
import socket
import threading

serverClients = list()  # Список клиентов


def sendMess(message, clSocket=None):
    # Отправляем сообщение всем, кроме автора
    for clientSocket, name in serverClients:
        if clientSocket != clSocket:
            try:
                clientSocket.send(message.encode('utf-8'))
            except Exception as e:
                print("Server Exception: ", e)
                removeClient(clientSocket)  # Удаляем клиента


def removeClient(clientSocket):
    for i, (sock, name) in enumerate(serverClients):
        if sock == clientSocket:
            serverClients.pop(i)
            try:
                sock.close()
            except Exception as e:
                print("Server Exception: ", e)
                pass

            print(f"Client {name} removed")
            sendMess(f'Client {name} gone')
            break


def meetClient(clSocket, address):
    try:
        name = clSocket.recv(1024).decode('utf-8')  # Получаем имя клиента для приветствия
        print(f"Client {name} added from address: {address}")

        serverClients.append((clSocket, name))  # Запоминаем клиента
        sendMess(f'Client {name} added in chat.', clSocket)  # Отправляем всем сообщение о подключении клиента

        # Читаем сообщения
        while True:
            try:

                message = clSocket.recv(1024).decode('utf-8')

                if not message:
                    break

                readyMessage = f'{name}: {message}'
                sendMess(readyMessage, clSocket)

            except Exception as e:
                print("Server Exception: ", e)
                break

    except Exception as e:
        print("Server Exception: ", e)
        clSocket.sendto(("Can't add you in chat. Exception: " + str(e)).encode('utf-8'))


serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Создаем сокет localhost 9090
serverSocket.bind(('', 9090))
serverSocket.listen(5)
serverSocket.settimeout(180)
print("Server is ready for work")

try:
    while True:
        clSocket, addr = serverSocket.accept()  # Принимаем подключение
        clientThread = threading.Thread(target=meetClient, args=(clSocket, addr),
                                        daemon=True)  # Создаем поток для подключенного клиента
        clientThread.start()

except Exception as e:
    print("Server Exception: ", e)

finally:
    for clSocket, name in serverClients:
        try:
            clSocket.close()
        except:
            pass
    serverSocket.close()
    print("Server stopped")
```

**Клиент:**

```python
import socket, threading

def receiveMessage(clientSocket):
    while True:
        try:
            message = clientSocket.recv(1024).decode('utf-8')

            if not message:
                print('No message')
                break

            print(message, flush=True)

        except Exception as e:
            print("Exception: ", e)

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    clientSocket.connect(('localhost', 9090))

    name = str(input("Введите свое имя:"))
    clientSocket.send(name.encode('utf-8'))

    # Поток для получения сообщений
    receiveThread = threading.Thread(target=receiveMessage, args=(clientSocket,), daemon=True)
    receiveThread.start()

    # Отправка сообщений
    while True:
        try:
            message = str(input())

            # Выход из чата
            if message == '':
                break

            clientSocket.send(message.encode('utf-8'))

        except Exception as e:
            print("Exception: ", e)
            break

except Exception as e:
    print("Client Exception: ", e)

finally:
    clientSocket.close()
```

**Пояснения:**

На **сервере** мы все также открываем сокет TCP на localhost 9090 и создаем список для хранения всех подключенных к чату
клиентов. Подключение к чату происходит автоматически, когда клиент соединяется с сервером, с помощью создания потока
для этого клиента с методом meetClient. Данный метод приветствует пользователя и остается читать входящие сообщения.
Как только сообщение получено, оно рассылается всем подключенным клиентам, или, если сообщение не получилось отправить,
адресат удаляется из списка клиентов.

На стороне **клиента**, при запуске, мы запрашиваем его имя и отправляем его серверу для приветствия. После чего запускаем
поток для приема сообщений и цикл для отправки сообщений. Если пользователь отправил пустую строку, значит он решил
выйти из чата.

## Задание 5

Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python.

Сервер должен:

* Принять и записать информацию о дисциплине и оценке по дисциплине.
* Отдать информацию обо всех оценках по дисциплинам в виде HTML-страницы.

### Реализация

**Сервер:**

```python
import socket
from email.parser import Parser
from students.k3341.Smirnova_Karina.Lab1.task5.Request import Request
from students.k3341.Smirnova_Karina.Lab1.task5.Response import Response

MAX_LINE = 64*1024
MAX_HEADERS = 100

# GET /marks
# POST /addMark?sub=Biology&mark=4

class MyHttpServer:
    def __init__(self, host, port, server_name):
        self.host = host
        self.port = port
        self.server_name = server_name
        self.marks = {}

    def serve_forever(self):
        """Запуск сервера на сокете, обработка входящих соединений"""

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            server_socket.bind((self.host, self.port))
            server_socket.listen()

            while True:
                client_socket, address = server_socket.accept()

                try:
                    self.serve_client(client_socket)

                except Exception as e:
                    print("Client serving failed: ", e)
        finally:
            server_socket.close()

    def serve_client(self, client_socket):
        """Обработка клиентского подключения"""

        try:
            request = self.parse_request(client_socket)
            response = self.handle_request(request)
            self.send_response(client_socket, response)

        except ConnectionResetError:
            client_socket = None
        except Exception as e:
            print('Error: ', e)
            self.send_error(client_socket, e)

        if client_socket:
            client_socket.close()

    def parse_request(self, client_socket):
        """Функция для обработки заголовка http запроса"""

        rfile = client_socket.makefile('rb')  # Обернули сокет в бинарный файл
        method, target, ver = self.parce_request_line(rfile)
        headers = self.parce_headers(rfile)

        host = headers.get('Host')
        if not host:
            raise Exception('Bad request')

        if host not in (self.server_name, f'{self.server_name}:{self.port}'):
            raise Exception('Not found host')

        return Request(method, target, ver, headers, rfile)

    def parce_request_line(self, rfile):
        """Обработка строки запроса"""

        raw = rfile.readline(MAX_LINE + 1)
        if len(raw) > MAX_LINE:
            raise Exception("Request line is too long")

        request_line = str(raw, 'iso-8859-1')
        request_line = request_line.strip('\r\n')
        words = request_line.split()
        if len(words) != 3:
            raise Exception('Wrong request format')

        method, target, ver = words
        if ver != 'HTTP/1.1':
            raise Exception("Unexpected HTTP version")

        return method, target, ver

    def parce_headers(self, rfile):
        """Обработка заголовков запроса"""

        headers = []

        while True:
            line = rfile.readline(MAX_LINE + 1)
            if len(line) > MAX_LINE:
                raise Exception('Header line is to loong')

            # Конец заголовков
            if line in (b'\r\n', b'\n', b''):
                break

            headers.append(line)

            if len(headers) > MAX_HEADERS:
                raise Exception('Too many headers')

        headers_dict = b''.join(headers).decode('iso-8859-1')

        return Parser().parsestr(headers_dict)

    def handle_request(self, request):
        """Обработка запроса"""

        if request.path == '/marks' and request.method == 'GET':
            return self.handle_get_marks(request)

        elif request.path == '/addMark' and request.method == 'POST' and 'sub' in request.query and 'mark' in request.query:
            return self.handle_post_addMark(request)

        else:
            raise Exception(f'Unknown path {request.path} or method {request.method}')

    def handle_get_marks(self, request):
        """Получение оценок"""

        accept = request.headers.get('Accept')
        if 'text/html' in accept:
            contentType = 'text/html; charset=utf-8'
            body = '<html><head></head><body>'
            body += f'<div>Оценки ({len(self.marks)})</div>'
            body += '<ul>'
            for sub, mark in self.marks.items():
                body += f'<li>{sub}: {mark}</li>'
            body += '</ul>'
            body += '</body></html>'

        else:
            return Response(406, 'Not Acceptable')

        body = body.encode('utf-8')
        headers = [('Content-Type', contentType),
                   ('Content-Length', len(body))]

        return Response(200, 'OK', headers, body)

    def handle_post_addMark(self, request):
        """Добавление предмета и оценки в список"""

        self.marks[request.query['sub'][0]] = float(request.query['mark'][0])
        return Response(204, 'Created')

    def send_response(self, client_socket, response):
        """Формирование HTTP ответа"""

        wfile = client_socket.makefile('wb')
        status_line = f'HTTP/1.1 {response.status} {response.reason}\r\n'
        wfile.write(status_line.encode('iso-8859-1'))

        if response.headers:
            for key, val in response.headers:
                header_line = f'{key}: {val}\r\n'
                wfile.write(header_line.encode('iso-8859-1'))

        wfile.write(b'\r\n')

        if response.body:
            wfile.write(response.body)

        wfile.flush()
        wfile.close()

    def send_error(self, client_socket, err):
        """Формирование страницы ошибки"""

        try:
            status = err.status
            reason = err.reason
            body = (err.body or err.reason).encode('utf-8')
        except:
            status = 500
            reason = b'Internal Server Error'
            body = b'Internal Server Error'

        resp = Response(status, reason,
                        [('Content-Length', len(body))],
                        body)
        self.send_response(client_socket, resp)

if __name__ == "__main__":
    host = '127.0.0.1'
    port = 9090
    name = 'serverName.com'

    server = MyHttpServer(host, port, name)
    try:
        server.serve_forever()
        print("Server is ready for work")
    except KeyboardInterrupt:
        pass
```

**Клиент:**

```python
import socket

get_request = """GET /marks HTTP/1.1\r
Host: serverName.com\r
Accept: text/html\r
\r
"""

while True:
    print("Выберете запрос:")
    print("1. GET Получить все оценки")
    print("2. POST Создать оценку")
    print("3. Выход")

    command = int(input())

    if command == 1:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('127.0.0.1', 9090))
            client_socket.send(get_request.encode('iso-8859-1'))

            response = client_socket.recv(1024).decode('utf-8')
            print(response, flush=True)

        except Exception as e:
            print("Exception: ", e)

        finally:
            client_socket.close()

    elif command == 2:
        print('Введите предмет и оценку через пробел')
        command = str(input())

        sub, mark = command.split()

        post_request = f"""POST /addMark?sub={sub}&mark={mark} HTTP/1.1\r
Host: serverName.com:9090\r
Content-Length: 0\r
\r
"""

        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('127.0.0.1', 9090))
            client_socket.send(post_request.encode('iso-8859-1'))

            response = client_socket.recv(1024).decode('utf-8')
            print(response, flush=True)
        except Exception as e:
            print("Exception: ", e)

        finally:
            client_socket.close()

    elif command == 3:
        break

    else:
        print('Unsupported command')
```

**Запрос:**

```python
from functools import lru_cache
from urllib.parse import parse_qs, urlparse

class Request:
    def __init__(self, method, target, version, headers, rfile):
        self.method = method
        self.target = target
        self.version = version
        self.headers = headers
        self.rfile = rfile

    @property
    def path(self):
        return self.url.path

    @property
    @lru_cache(maxsize=None)
    def query(self):
        return parse_qs(self.url.query)

    @property
    @lru_cache(maxsize=None)
    def url(self):
        return urlparse(self.target)

    def __str__(self):
        return f"Request(method={self.method}, target={self.target}, version={self.version})"

```

**Ответ:**

```python
class Response:
    def __init__(self, status, reason, headers=None, body=None):
        self.status = status
        self.reason = reason
        self.headers = headers
        self.body = body

    def __str__(self):
        return f"Response(status={self.status}, reason={self.reason}, body_length={len(self.body) if self.body else 0})"
```

**Пояснения:**

**MyHttpServer - класс сервера**, который создается на localhost порт 9090 и хранит словарь с оценками. Запускаем сервер
с помощью метода serve_forever() и в бесконечном цикле обрабатываем HTTP-запросы от клиента с помощью метода
serve_client. В этом методе мы обрабатываем запрос, формируем ответ, отправляем его клиенту и закрываем соединение.

В методе parse_request для обработки заголовка и строки запроса мы оборачиваем сокет в бинарный файл, из которого
считываем запрос построчно. Если все обработано без ошибок, то формируем запрос - объект класса Request.

Сформированный запрос отправляется в метод handle_request для обработки запроса: Get запрос на получение вех оценок и
POST запрос на добавление предмета и оценки. На выходе мы получаем ответ - экземпляр класса Response.

Сформированный ответ отправляется в метод send_response, в котором тело ответа оборачивается в заголовок и отправляется.

Если на каком-то из этапов у нас появляется ошибка, то с помощью метода send_error мы формируем ответ как страницу
ошибки.

**Для клиента** есть меню выбора: сделать Get или Post запрос, или выйти из программы.