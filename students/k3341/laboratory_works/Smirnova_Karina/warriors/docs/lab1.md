# Отчет по лабораторной работе №1

## Задание 1

**Условие:**  
Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.  
**Требования:**  
- Использовать библиотеку `socket`
- Протокол UDP

### Сервер

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

### Клиент

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

### Пояснения

- Сервер открывает UDP сокет на localhost:9090. В бесконечном цикле читает сообщения от клиентов, декодирует и печатает их, а затем отправляет ответ.
- Клиент создает UDP сокет, отправляет сообщение на сервер и ждет ответа.


---

## Задание 2

**Условие:**  
Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции (вычисление гипотенузы), параметры вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.  
**Требования:**  
- Использовать библиотеку `socket`
- Протокол TCP

### Сервер

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

### Клиент

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

### Пояснения

- На сервере реализована функция для вычисления гипотенузы. Сервер ждет соединения, читает данные, вычисляет результат и отправляет клиенту.
- Клиент отправляет серверу две стороны прямоугольника, получает и выводит результат.

---

## Задание 3

**Условие:**  
Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которую сервер подгружает из файла `index.html`.  
**Требования:**  
- Использовать библиотеку `socket`

### Сервер

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

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', 9090))
serverSocket.listen(3)
serverSocket.settimeout(60)

try:
    while True:
        clSocket, addr = serverSocket.accept()
        try:
            request = clSocket.recv(1024).decode("utf-8")
            htmlText = readPage()
            http_response = makeResponse(htmlText)
            clSocket.send(http_response.encode('utf-8'))
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

### Клиент

```python
import socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    clientSocket.connect(('localhost', 9090))
    http_request = """
    GET /index.html HTTP/1.1
    HOST: localhost 9090
    """
    clientSocket.send(http_request.encode('utf-8'))
    response = ''
    while True:
        part = clientSocket.recv(1024).decode('utf-8')
        if not part:
            break
        response += part
    print("Response:\n", response)
except Exception as e:
    print("Exception: ", e)
finally:
    clientSocket.close()
```

### index.html

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

### Пояснения

- Сервер открывает TCP сокет на localhost:9090, читает файл index.html и формирует HTTP-ответ.
- Клиент отправляет HTTP GET запрос и выводит полученную страницу.

---

## Задание 4

**Условие:**  
Реализовать двухпользовательский или многопользовательский чат. Для максимального количества баллов реализуйте многопользовательский чат.  
**Требования:**  
- Использовать библиотеку `socket`
- Для многопользовательского чата использовать `threading`
- Протокол TCP: 100% баллов

### Сервер

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
                removeClient(clientSocket)

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
        name = clSocket.recv(1024).decode('utf-8')
        print(f"Client {name} added from address: {address}")
        serverClients.append((clSocket, name))
        sendMess(f'Client {name} added in chat.', clSocket)
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

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', 9090))
serverSocket.listen(5)
serverSocket.settimeout(180)
print("Server is ready for work")

try:
    while True:
        clSocket, addr = serverSocket.accept()
        clientThread = threading.Thread(target=meetClient, args=(clSocket, addr), daemon=True)
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

### Клиент

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
    receiveThread = threading.Thread(target=receiveMessage, args=(clientSocket,), daemon=True)
    receiveThread.start()
    while True:
        try:
            message = str(input())
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

### Пояснения

- Сервер хранит список клиентов, каждому клиенту создается отдельный поток.
- Клиент отправляет свое имя, далее запускает отдельный поток для приема сообщений и цикл для отправки сообщений.


---

## Задание 5

**Условие:**  
Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python.  
**Сервер должен:**  
- Принять и записать информацию о дисциплине и оценке по дисциплине.
- Отдать информацию обо всех оценках по дисциплинам в виде HTML-страницы.

### Сервер

```python
import socket
from urllib.parse import parse_qs
from email.parser import Parser
from students.k3341.Smirnova_Karina.Lab1.task5.Request import Request
from students.k3341.Smirnova_Karina.Lab1.task5.Response import Response

MAX_LINE = 64*1024
MAX_HEADERS = 100

class MyHttpServer:
    def __init__(self, host, port, server_name):
        self.host = host
        self.port = port
        self.server_name = server_name
        self.marks = {}

    def serve_forever(self):
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
        rfile = client_socket.makefile('rb')
        method, target, ver = self.parce_request_line(rfile)
        headers = self.parce_headers(rfile)
        host = headers.get('Host')
        if not host:
            raise Exception('Bad request')
        if host not in (self.host, f'{self.host}:{self.port}', self.server_name, f'{self.server_name}:{self.port}'):
            raise Exception('Not found host')
        request = Request(method, target, ver, headers, rfile)
        if method == 'POST':
            form_fields = self.parse_post_form(request)
            request.form = form_fields
        return request

    def parce_request_line(self, rfile):
        raw = rfile.readline(MAX_LINE + 1)
        if len(raw) > MAX_LINE:
            raise Exception("Request line is too long")
        request_line = str(raw, 'iso-8859-1').strip('\r\n')
        words = request_line.split()
        if len(words) != 3:
            raise Exception('Wrong request format')
        method, target, ver = words
        if ver != 'HTTP/1.1':
            raise Exception("Unexpected HTTP version")
        return method, target, ver

    def parce_headers(self, rfile):
        headers = []
        while True:
            line = rfile.readline(MAX_LINE + 1)
            if len(line) > MAX_LINE:
                raise Exception('Header line is to loong')
            if line in (b'\r\n', b'\n', b''):
                break
            headers.append(line)
            if len(headers) > MAX_HEADERS:
                raise Exception('Too many headers')
        headers_dict = b''.join(headers).decode('iso-8859-1')
        return Parser().parsestr(headers_dict)

    def parse_post_form(self, request):
        content_length = int(request.headers.get('Content-Length', 0))
        if content_length > 0:
            body = request.rfile.read(content_length).decode('utf-8')
            return parse_qs(body)
        return {}

    def handle_request(self, request):
        if request.path == '/marks' and request.method == 'GET':
            return self.handle_get_marks(request)
        elif request.path == '/addMark' and request.method == 'POST':
            return self.handle_post_addMark(request)
        else:
            raise Exception(f'Unknown path {request.path} or method {request.method}')

    def handle_get_marks(self, request):
        accept = request.headers.get('Accept')
        if 'text/html' in accept:
            contentType = 'text/html; charset=utf-8'
            body = '<html><head></head><body>'
            body += f'<div>Оценки ({len(self.marks)})</div>'
            body += '<ul>'
            for sub, marks in self.marks.items():
                marks_str = ', '.join(str(m) for m in marks)
                body += f'<li>{sub}: {marks_str}</li>'
            body += '</ul>'
            body += '''
                    <h3>Добавить оценку</h3>
                    <form action="/addMark" method="POST">
                        <label>Предмет: <input type="text" name="sub" required></label><br>
                        <label>Оценка: <input type="number" name="mark" step="any" required></label><br>
                        <button type="submit">Добавить</button>
                    </form>
                    '''
            body += '</body></html>'
        else:
            return Response(406, 'Not Acceptable')
        body = body.encode('utf-8')
        headers = [('Content-Type', contentType),
                   ('Content-Length', len(body))]
        return Response(200, 'OK', headers, body)

    def handle_post_addMark(self, request):
        subject = request.form['sub'][0]
        mark = float(request.form['mark'][0])
        if subject not in self.marks:
            self.marks[subject] = []
        self.marks[subject].append(mark)
        headers = [('Location', '/marks')]
        return Response(303, 'Redirect', headers)

    def send_response(self, client_socket, response):
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
    host = 'localhost'
    port = 8080
    name = 'serverName.com'
    server = MyHttpServer(host, port, name)
    try:
        server.serve_forever()
        print("Server is ready for work")
    except KeyboardInterrupt:
        pass
```

### Request

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
        self.form = {}

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

### Response

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

### Пояснения

- Класс `MyHttpServer` реализует сервер, который хранит оценки по дисциплинам.  
- Сервер принимает GET-запросы на `/marks` для отображения всех оценок в виде HTML-страницы, и POST-запросы на `/addMark` для добавления оценки.
- Парсинг HTTP-запроса ведется вручную, формируется объект `Request`.
- Ответ формируется с помощью класса `Response` и отправляется клиенту.
- В случае ошибки отправляется страница ошибки.