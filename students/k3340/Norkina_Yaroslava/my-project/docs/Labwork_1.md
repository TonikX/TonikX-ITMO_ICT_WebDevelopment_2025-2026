Отчет

Лабораторная работа №1 «**Работа с сокетами.**»

Цель: понимание того, как происходит сетевое взаимодействие различных
сокетов, используемых при передаче данных.

Программное обеспечение: Python 3.6+.

Практические задания.

**Задание 1:**

Реализована клиентская и серверная части приложения.

Клиент отправляет серверу сообщение «Hello, server», и оно должно
отобразиться на стороне сервера.

client.py:

import socket

\# Создаем сокет

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

\# Отправляем сообщение серверу

client_socket.sendto(b\'Hello, server!\', (socket.gethostname(), 8080))

\# Получаем ответ от сервера

response, server_address = client_socket.recvfrom(1024)

print(f\'Ответ от сервера: {response.decode()}\')

\# Закрываем сокет

client_socket.close()

В ответ сервер отправляет клиенту сообщение «Hello, client», которое
должно отобразиться у клиента.

server.py:

import socket

\# Создаем сокет

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

\# Привязываем сокет к адресу и порту

server_socket.bind((socket.gethostname(), 8080))

print(\"Сервер запущен на порту 8080\...\")

while True:

    \# Получаем сообщение от клиента

    request, client_address = server_socket.recvfrom(1024)

    request = request.decode()

    print(f\'Запрос от клиента {client_address}: {request}\')

    \# Отправляем ответ клиенту

    response = \'Hello, client!\'

    server_socket.sendto(response.encode(), client_address)

Выполнены требования:

-   Обязательно использовать библиотеку socket.

-   Реализовать с помощью протокола UDP: **socket.SOCK_DGRAM** -- тип
    сокета, который используется для работы с протоколом UDP (User
    Datagram Protocol) в сетевом программировании. UDP работает без
    установления соединения, данные передаются в виде отдельных
    сообщений (датаграмм). При этом используется семейство адресов IPv4
    (AF_INET).

Демонстрация работы:

![Изображение выглядит как текст, снимок экрана, Шрифт Содержимое,
созданное искусственным интеллектом, может быть
неверным.](media/image1.png){width="6.496527777777778in"
height="0.8180555555555555in"}

Запускаем клиента:

![Изображение выглядит как текст, снимок экрана, Шрифт, черный
Содержимое, созданное искусственным интеллектом, может быть
неверным.](media/image2.png){width="6.496527777777778in"
height="0.8701388888888889in"}

![Изображение выглядит как текст, снимок экрана, Шрифт Содержимое,
созданное искусственным интеллектом, может быть
неверным.](media/image3.png){width="6.496527777777778in"
height="0.9361111111111111in"}

**Задание 2:**

Реализована клиентская и серверная части приложения.

1.  **Вариант** Теорема Пифагора.

Клиент запрашивает выполнение математической операции, параметры которой
(длины сторон прямоугольного треугольника) вводятся с клавиатуры.

client.py:

import socket

\# Создаем сокет

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

\# Подключаемся к серверу

client_socket.connect((socket.gethostname(), 8080))

\# Считываем строку вида \"a b\" - длины сторон треугольника

a=input().encode(\'utf-8\')

\# Отправляем сообщение серверу

client_socket.sendall(a)

\# Получаем ответ от сервера

response = client_socket.recv(1024)

print(f\'Ответ от сервера: {response.decode()}\')

\# Закрываем соединение

client_socket.close()

Сервер обрабатывает данные и возвращает результат клиенту.

server.py:

import math

import socket

\# Создаем сокет

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

\# Привязываем сокет к адресу и порту

server_socket.bind((socket.gethostname(), 8080))

\# Начинаем слушать входящие подключения (ожидание клиентов)

server_socket.listen(1)

print(\"Сервер запущен на порту 8080\...\")

while True:

    \# Принимаем соединение от клиента

    client_connection, client_address = server_socket.accept()

    print(f\'Подключение от {client_address}\')

    \# Получаем сообщение от клиента

    request = client_connection.recv(1024).decode()

    a,b=request.split()

    a=int(a)

    b=int(b)

    \# Отправляем ответ клиенту

    response = str(math.sqrt(a\*\*2 + b\*\*2))

    client_connection.sendall(response.encode())

    \# Закрываем соединение

    client_connection.close()

**Выполнены требования:**

-   Обязательно использовать библиотеку socket.

-   Реализовать с помощью протокола TCP: socket.**SOCK_STREAM** -- это
    тип сокета, который указывает на **протокол TCP (Transmission
    Control Protocol)**. TCP-сокеты обеспечивают надёжную, упорядоченную
    доставку данных. 

Протестируем сервер:

![Изображение выглядит как текст, снимок экрана, Шрифт Содержимое,
созданное искусственным интеллектом, может быть
неверным.](media/image4.png){width="6.496527777777778in"
height="0.9222222222222223in"}

Запустим клиента:

![Изображение выглядит как текст, снимок экрана, Шрифт, черный
Содержимое, созданное искусственным интеллектом, может быть
неверным.](media/image5.png){width="6.496527777777778in"
height="0.8694444444444445in"}

Получаем правильный ответ, соединение установлено.

![Изображение выглядит как текст, снимок экрана, Шрифт, линия
Содержимое, созданное искусственным интеллектом, может быть
неверным.](media/image6.png){width="3.3274682852143482in"
height="0.6221642607174104in"}

**Задание 3:**

Реализована серверная часть приложения. Клиент подключается к серверу, и
в ответ получает HTTP-сообщение, содержащее HTML-страницу, которуя
сервер подгружает из файла index.html.

server.py:

import socket

\# Параметры сервера

HOST = \'localhost\'

PORT = 8080

\# Создаем сокет

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen(5)

print(f\"HTTP сервер запущен на {HOST}:{PORT}\...\")

\# Функция для чтения HTML-файла

def load_html_file(filename):

    try:

        with open(filename, \'r\', encoding=\'utf-8\') as file:

            return file.read()

    except FileNotFoundError:

        \# Если файл не найден, возвращаем текст ошибки 404

        return \"\<h1\>404 Not Found\</h1\>\<p\>Файл index.html не
найден.\</p\>\"

while True:

    client_connection, client_address = server_socket.accept()

    print(f\'Подключение от {client_address}\')

    request = client_connection.recv(1024).decode()

    print(f\'Запрос клиента:\\n{request}\')

    \# Загружаем содержимое index.html

    html_content = load_html_file(\'index.html\')

    \# Формируем HTTP-ответ

    http_response = (

        \"HTTP/1.1 200 OK\\r\\n\"

        \"Content-Type: text/html; charset=UTF-8\\r\\n\"

        f\"Content-Length: {len(html_content)}\\r\\n\"

        \"Connection: close\\r\\n\"

        \"\\r\\n\"

        + html_content

    )

    client_connection.sendall(http_response.encode())

    client_connection.close()

**Выполнены требования:**

-   Обязательно использовать библиотеку socket.

Запустим сервер:

![](media/image7.png){width="6.496527777777778in"
height="0.3784722222222222in"}

![](media/image8.png){width="6.496527777777778in"
height="2.0243055555555554in"}

**Задание 4:**

Был реализован многопользовательский чат. Выполнены требования:

-   Обязательно использовать библиотеку socket.

-   Для многопользовательского чата необходимо использовать
    библиотеку threading.

**Реализация:**

client.py:

\# chat_client.py

import socket

import threading

import sys

def receive_messages(client_socket):

    \"\"\"Получает и выводит входящие сообщения\"\"\"

    while True:

        try:

            message = client_socket.recv(1024).decode(\'utf-8\')

            if not message:

                break

            print(message)

        except ConnectionResetError:

            print(\"\[!\] Соединение с сервером потеряно.\")

            break

        except OSError:

            break  # Сокет закрыт

def main():

    HOST = \'localhost\'

    PORT = 12345

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:

        client.connect((HOST, PORT))

        print(\"\[\*\] Подключено к чату. Введите своё имя:\")

        username = input().strip()

        if not username:

            username = \"Anonymous\"

        \# Запускаем поток для получения сообщений

        recv_thread = threading.Thread(target=receive_messages,
args=(client,))

        recv_thread.daemon = True

        recv_thread.start()

        print(f\"\[+\] Привет, {username}! Вводите сообщения (Ctrl+C или
exit для выхода):\")

        while True:

            try:

                msg = input()

                if msg.lower() == \'exit\':

                    break

                full_message = f\"{username}: {msg}\"

                client.send(full_message.encode(\'utf-8\'))

            except KeyboardInterrupt:

                break

    except ConnectionRefusedError:

        print(\"\[!\] Не удалось подключиться к серверу.\")

    finally:

        client.close()

        print(\"\[\*\] Отключено.\")

if \_\_name\_\_ == \"\_\_main\_\_\":

    main()

server.py:

\# chat_server.py

import socket

import threading

\# Глобальный список подключённых клиентов: (client_socket, address)

clients = \[\]

clients_lock = threading.Lock()  # Для безопасного доступа из нескольких
потоков

def broadcast(message, sender_socket=None):

    \"\"\"Рассылает сообщение всем клиентам, кроме отправителя (если
указан)\"\"\"

    with clients_lock:

        for client_socket, \_ in clients\[:\]:  # Копия списка на случай
удаления

            if client_socket != sender_socket:

                try:

                    client_socket.send(message)

                except Exception:

                    \# Если клиент отключился --- удаляем его

                    client_socket.close()

                    clients\[:\] = \[(sock, addr) for sock, addr in
clients if sock != client_socket\]

def handle_client(client_socket, address):

    \"\"\"Обрабатывает одного клиента в отдельном потоке\"\"\"

    print(f\"\[+\] Новое подключение: {address}\")

    with clients_lock:

        clients.append((client_socket, address))

    try:

        while True:

            message = client_socket.recv(1024)

            if not message:

                break

            print(f\"\[{address}\] {message.decode(\'utf-8\',
errors=\'replace\')}\")

            broadcast(message, sender_socket=client_socket)

    except ConnectionResetError:

        pass

    finally:

        with clients_lock:

            clients\[:\] = \[(sock, addr) for sock, addr in clients if
sock != client_socket\]

        client_socket.close()

        print(f\"\[-\] Клиент отключён: {address}\")

def main():

    HOST = \'localhost\'

    PORT = 12345

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((HOST, PORT))

    server.listen()

    print(f\"\[\*\] Сервер запущен на {HOST}:{PORT}\")

    try:

        while True:

            client_socket, addr = server.accept()

            thread = threading.Thread(target=handle_client,
args=(client_socket, addr))

            thread.daemon = True  # Поток завершится при выходе из main

            thread.start()

    except KeyboardInterrupt:

        print(\"\\n\[!\] Сервер остановлен.\")

    finally:

        server.close()

if \_\_name\_\_ == \"\_\_main\_\_\":

    main()

-   Протокол TCP: для TCP созданы клиентские подключения и обработка
    сообщений от всех пользователей в потоках. Каждый клиент
    подключается к серверу, и все сообщения автоматически рассылаются
    остальным участникам чата.

-   SOCK_STREAM -- использование **TCP**

-   client_socket, addr = server.accept() -- выполняется трёхэтапное
    рукопожатие TCP, создаётся новый сокет. Сервер принимает входящее
    соединение.

-   thread = threading.Thread(target=handle_client, args=(client_socket,
    addr)); thread.start() -- библиотека threading используется для
    создания нового потока, чтобы не блокировать основной цикл сервера.

-   Автоматическое удаление отключившихся клиентов при ошибках отправки.

Запустим сервер:

![Изображение выглядит как текст, снимок экрана, Шрифт Содержимое,
созданное искусственным интеллектом, может быть
неверным.](media/image9.png){width="6.496527777777778in"
height="1.0875in"}

Создадим несколько клиентов и пользователей в чате:

![Изображение выглядит как текст, снимок экрана, черный, Шрифт
Содержимое, созданное искусственным интеллектом, может быть
неверным.](media/image10.png){width="6.496527777777778in"
height="1.0798611111111112in"}

![Изображение выглядит как текст, снимок экрана, Шрифт, черный
Содержимое, созданное искусственным интеллектом, может быть
неверным.](media/image11.png){width="6.496527777777778in"
height="1.2020833333333334in"}

![Изображение выглядит как текст, снимок экрана, Шрифт Содержимое,
созданное искусственным интеллектом, может быть
неверным.](media/image12.png){width="6.496527777777778in"
height="1.038888888888889in"}

![Изображение выглядит как текст, снимок экрана, Шрифт Содержимое,
созданное искусственным интеллектом, может быть
неверным.](media/image13.png){width="6.496527777777778in"
height="1.48125in"}

На сервере отображаются все сообщения:

![Изображение выглядит как текст, снимок экрана, Шрифт, дизайн
Содержимое, созданное искусственным интеллектом, может быть
неверным.](media/image14.png){width="5.0741218285214345in"
height="2.5563156167979004in"}

**Задание 5:**

Написать простой веб-сервер для обработки GET и POST HTTP-запросов с
помощью библиотеки socket в Python. Сервер должен:

-   Принять и записать информацию о дисциплине и оценке по дисциплине.

-   Отдать информацию обо всех оценках по дисциплинам в виде
    HTML-страницы.

Реализация:

server.py:

import json

import socket

import sys

from email.parser import Parser

from functools import lru_cache

from urllib.parse import parse_qs, urlparse

MAX_LINE = 64 \* 1024

MAX_HEADERS = 100

class MyHTTPServer:

    def \_\_init\_\_(self, host, port, server_name):

        self.\_host = host

        self.\_port = port

        self.\_server_name = server_name

        self.\_grades = \[\]  # Список: \[{\'discipline\': \'\...\',
\'grade\': \'\...\'}, \...\]

    def serve_forever(self):

        serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:

            serv_sock.bind((self.\_host, self.\_port))

            serv_sock.listen()

            print(f\"Сервер запущен:
http://{self.\_host}:{self.\_port}/grades\")

            while True:

                conn, \_ = serv_sock.accept()

                try:

                    self.serve_client(conn)

                except Exception as e:

                    print(\'Ошибка при обработке клиента:\', e)

        finally:

            serv_sock.close()

    def serve_client(self, conn):

        try:

            req = self.parse_request(conn)

            resp = self.handle_request(req)

            self.send_response(conn, resp)

        except ConnectionResetError:

            pass

        except Exception as e:

            self.send_error(conn, e)

        finally:

            if conn:

                try:

                    req.rfile.close()

                except:

                    pass

                conn.close()

    def parse_request(self, conn):

        rfile = conn.makefile(\'rb\')

        method, target, ver = self.parse_request_line(rfile)

        headers = self.parse_headers(rfile)

        host = headers.get(\'Host\')

        if not host:

            raise HTTPError(400, \'Bad Request\', \'Заголовок Host
обязателен\')

        if host not in (self.\_server_name,
f\'{self.\_server_name}:{self.\_port}\'):

            raise HTTPError(404, \'Not Found\')

        return Request(method, target, ver, headers, rfile)

    def parse_request_line(self, rfile):

        raw = rfile.readline(MAX_LINE + 1)

        if len(raw) \> MAX_LINE:

            raise HTTPError(400, \'Bad Request\', \'Слишком длинная
строка запроса\')

        req_line = str(raw, \'iso-8859-1\')

        words = req_line.rstrip(\'\\r\\n\').split()

        if len(words) != 3:

            raise HTTPError(400, \'Bad Request\', \'Некорректная строка
запроса\')

        method, target, ver = words

        if ver != \'HTTP/1.1\':

            raise HTTPError(505, \'HTTP Version Not Supported\')

        return method, target, ver

    def parse_headers(self, rfile):

        headers = \[\]

        while True:

            line = rfile.readline(MAX_LINE + 1)

            if len(line) \> MAX_LINE:

                raise HTTPError(494, \'Request header too large\')

            if line in (b\'\\r\\n\', b\'\\n\', b\'\'):

                break

            headers.append(line)

            if len(headers) \> MAX_HEADERS:

                raise HTTPError(494, \'Too many headers\')

        sheaders = b\'\'.join(headers).decode(\'iso-8859-1\')

        return Parser().parsestr(sheaders)

    def handle_request(self, req):

        if req.path == \'/grades\' and req.method == \'POST\':

            return self.handle_post_grade(req)

        if req.path == \'/grades\' and req.method == \'GET\':

            return self.handle_get_grades(req)

        raise HTTPError(404, \'Not Found\')

    def handle_post_grade(self, req):

        discipline = req.query.get(\'discipline\', \[None\])\[0\]

        grade = req.query.get(\'grade\', \[None\])\[0\]

        if not discipline or not grade:

            raise HTTPError(400, \'Bad Request\', \'Требуются параметры:
discipline и grade\')

        \# Опционально: проверка, что grade --- число от 1 до 5

        try:

            grade_int = int(grade)

            if not (1 \<= grade_int \<= 5):

                raise ValueError

        except ValueError:

            raise HTTPError(400, \'Bad Request\', \'Оценка должна быть
целым числом от 1 до 5\')

        self.\_grades.append({\'discipline\': discipline, \'grade\':
grade_int})

        return Response(204, \'Created\')

    def handle_get_grades(self, req):

        accept = req.headers.get(\'Accept\', \'\')

        if \'text/html\' in accept:

            contentType = \'text/html; charset=utf-8\'

            body = \'\<html\>\<head\>\<meta
charset=\"utf-8\"\>\<title\>Оценки\</title\>\</head\>\<body\>\'

            body += \'\<h2\>Список оценок\</h2\>\'

            if self.\_grades:

                body += \'\<ul\>\'

                for item in self.\_grades:

                    body +=
f\'\<li\>\<strong\>{item\[\"discipline\"\]}:\</strong\>
{item\[\"grade\"\]}\</li\>\'

                body += \'\</ul\>\'

            else:

                body += \'\<p\>Нет записей.\</p\>\'

            body += \'\<hr\>\<a href=\"/\"\>Обновить\</a\>\'

            body += \'\</body\>\</html\>\'

        elif \'application/json\' in accept:

            contentType = \'application/json; charset=utf-8\'

            body = json.dumps(self.\_grades, ensure_ascii=False)

        else:

            return Response(406, \'Not Acceptable\')

        body = body.encode(\'utf-8\')

        headers = \[

            (\'Content-Type\', contentType),

            (\'Content-Length\', len(body))

        \]

        return Response(200, \'OK\', headers, body)

    def send_response(self, conn, resp):

        wfile = conn.makefile(\'wb\')

        status_line = f\'HTTP/1.1 {resp.status} {resp.reason}\\r\\n\'

        wfile.write(status_line.encode(\'iso-8859-1\'))

        if resp.headers:

            for key, value in resp.headers:

                wfile.write(f\'{key}:
{value}\\r\\n\'.encode(\'iso-8859-1\'))

        wfile.write(b\'\\r\\n\')

        if resp.body:

            wfile.write(resp.body)

        wfile.flush()

        wfile.close()

    def send_error(self, conn, err):

        try:

            status = err.status

            reason = err.reason

            body = (err.body or reason).encode(\'utf-8\')

        except:

            status = 500

            reason = \'Internal Server Error\'

            body = b\'Internal Server Error\'

        headers = \[(\'Content-Length\', len(body))\]

        resp = Response(status, reason, headers, body)

        self.send_response(conn, resp)

class Request:

    def \_\_init\_\_(self, method, target, version, headers, rfile):

        self.method = method

        self.target = target

        self.version = version

        self.headers = headers

        self.rfile = rfile

    \@property

    def path(self):

        return self.url.path

    \@property

    \@lru_cache(maxsize=None)

    def query(self):

        return parse_qs(self.url.query)

    \@property

    \@lru_cache(maxsize=None)

    def url(self):

        return urlparse(self.target)

    def body(self):

        size = self.headers.get(\'Content-Length\')

        if not size:

            return None

        return self.rfile.read(int(size))

class Response:

    def \_\_init\_\_(self, status, reason, headers=None, body=None):

        self.status = status

        self.reason = reason

        self.headers = headers or \[\]

        self.body = body

class HTTPError(Exception):

    def \_\_init\_\_(self, status, reason, body=None):

        super()

        self.status = status

        self.reason = reason

        self.body = body

if \_\_name\_\_ == \'\_\_main\_\_\':

    if len(sys.argv) != 4:

        print(\"Использование: python grade_server.py \<host\> \<port\>
\<server_name\>\")

        print(\"Пример: python grade_server.py localhost 8080
localhost\")

        sys.exit(1)

    host = sys.argv\[1\]

    port = int(sys.argv\[2\])

    name = sys.argv\[3\]

    server = MyHTTPServer(host, port, name)

    try:

        server.serve_forever()

    except KeyboardInterrupt:

        print(\"\\nСервер остановлен.\")

**Хранение данных происходит в** оперативной памяти сервера в виде
списка словарей, где каждый элемент -- это словарь с двумя ключами
discipline и grade. Когда клиент отправляет данные, сервер обрабатывает
их в методе handle_post_grade(): **в нем извлекаются параметры с
использованием** класса Request, который парсит строку запроса, также
используется parse_qs() из urllib.parse для разбора параметров. В
результате отправки данных клиентом сервер сохраняет новый словарь вида
{\'discipline\': \[\'Математика\'\], \'grade\': \[\'5\'\]}. После
происходит добавление в конец списка всех сохраненных словарей
self.\_grades и возвращается ответ "204 No Content" (успешно, но без
тела ответа) на запрос клиенту.

**Как отдаётся информация обо всех оценках в виде HTML-страницы**

Функция handle_get_grades(self, req) обрабатывает GET-запрос от клиента,
смотрит на заголовок Accept в запросе и если клиент хочет text/html, то
отдаёт HTML, если application/json -- отдаёт JSON. Далее **строится
страница:**

1.  Базовая структура HTML с заголовком \<title\>Оценки\</title\>

2.  Заголовок \<h2\>Список оценок\</h2\>

3.  Создаётся ненумерованный список \<ul\>, если есть оценки

4.  Для каждой оценки создаётся элемент \<li\> в формате
    «**Дисциплина:** оценка»

5.  Если оценок нет -- показывается сообщение \"Нет записей\"

6.  Создается ссылка для обновления страницы

После этого **отправляется ответ клиенту со с**татусом 200 OK,
заголовками Content-Type и Content-Length и телом ответа (UTF-8).

Запустим сервер:

py MyHttpServer.py localhost 8080 localhost

![](media/image15.png){width="6.496527777777778in"
height="0.6027777777777777in"}

Добавим несколько дисциплин и оценок по предметам через командную
строку:

curl -X POST \"http://localhost:8080/grades?discipline=Web&grade=4\"

![Изображение выглядит как текст, снимок экрана, Шрифт Содержимое,
созданное искусственным интеллектом, может быть
неверным.](media/image16.png){width="6.496527777777778in"
height="1.7326388888888888in"}

Перейдем по ссылке <http://localhost:8080/grades>

![Изображение выглядит как текст, снимок экрана, Шрифт Содержимое,
созданное искусственным интеллектом, может быть
неверным.](media/image17.png){width="6.496527777777778in"
height="1.1847222222222222in"}
