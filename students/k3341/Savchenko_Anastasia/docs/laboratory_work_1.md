# Лабораторная работа 1. Работа с сокетами.

## Задание 1

Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.

### Требования:

- Обязательно использовать библиотеку socket.
- Реализовать с помощью протокола UDP.

### Реализация

**Серверная часть:**

```py title="udp_server.py" 
import socket

# Создаем UDP сокет
# AF_INET - используем IPv4
# SOCK_DGRAM - указываем UDP протокол
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # SOCK_DGRAM --> UDP протокол

# Привязываем сокет к адресу и порту
server.bind(('localhost', 1234))

# Получаем сообщение от клиента
# recvfrom возвращает (данные, адрес_клиента)
message_client, address_client = server.recvfrom(1024)

# Декодируем и выводим сообщение
print(message_client.decode('utf-8'))

# Отправляем ответ клиенту
server.sendto("Hello, client".encode('utf-8'), address_client)

# Закрываем соединение
server.close()
```

**Клиентская часть:**

```py title="udp_client.py" 
import socket

# Создаем UDP сокет
# AF_INET - используем IPv4
# SOCK_DGRAM - указываем UDP протокол
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Отправляем сообщение серверу
# sendto принимает (данные, (адрес, порт))
client.sendto("Hello, server".encode('utf-8'), ('localhost', 1234))

# Получаем ответ от сервера
# recvfrom возвращает (данные, адрес_сервера)
print(client.recvfrom(1024)[0].decode('utf-8'))

# Закрываем соединение
client.close()
```

### Пример выполнения:
1. Запустите сервер: `python udp_server.py`
2. Запустите клиент: `python udp_client.py`
3. На стороне сервера отобразится: `Hello, server`
4. На стороне клиента отобразится: `Hello, client`

### Вывод по заданию: 
Для выполнения задания 1 созданы два файла: udp_server.py (сервер) и udp_client.py (клиент). Сервер инициализирует UDP-сокет, выполняет привязку к localhost:1234 и ожидает данные. Клиент создает аналогичный UDP-сокет, передает сообщение "Hello, server" и переходит в режим приема ответа. При запуске программ в правильном порядке (сначала сервер, затем клиент) сервер получает сообщение, выводит его в консоль, отправляет ответное "Hello, client", которое клиент принимает и отображает. Задание выполнено успешно — продемонстрирована работа UDP-сокетов в клиент-серверной архитектуре.

### Полезные ссылки:
▶️ [TCP vs UDP Sockets in Python](https://www.youtube.com/watch?v=esLgiMLbRkI)

## Задание 2

Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

### Варианты операций:

- Теорема Пифагора
- Решение квадратного уравнения
- Поиск площади трапеции
- ✅ Поиск площади параллелограмма

### Требования:

- Обязательно использовать библиотеку socket.
- Реализовать с помощью протокола TCP.

### Реализация

**Серверная часть:**

```py title="tcp_math_server.py" 
import socket

# Функция вычисления площади параллелограмма
# Формула: S = a * h
# где a - основание, h - высота
def calculate_area(base, height):
    return base * height


# Создаем TCP сокет
# AF_INET - используем IPv4
# SOCK_STREAM - указываем TCP протокол
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет к адресу и порту
server.bind(('localhost', 1235))

# Начинаем прослушивание соединений
server.listen(1)

# Бесконечный цикл для обработки клиентских запросов
while True:
    # Принимаем соединение от клиента
    conn, _ = server.accept()
    
    # Получаем данные от клиента (основание и высоту)
    data = conn.recv(1024).decode()

    # Разделяем полученные данные на основание и высоту
    base, height = map(float, data.split())
    
    # Вычисляем площадь параллелограмма
    area = calculate_area(base, height)

    # Отправляем результат клиенту
    conn.send(str(area).encode())
    
    # Закрываем соединение с клиентом
    conn.close()
```

**Клиентская часть:**

```py title="tcp_math_client.py" 
import socket

# Создаем TCP сокет
# AF_INET - используем IPv4
# SOCK_STREAM - указываем TCP протокол
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Устанавливаем соединение с сервером
client.connect(('localhost', 1235))

# Запрашиваем у пользователя данные для вычисления
base = float(input("Основание: "))
height = float(input("Высота: "))

# Отправляем данные на сервер в формате "основание высота"
client.send(f"{base} {height}".encode())

# Получаем результат от сервера
result = client.recv(1024).decode()

# Выводим результат вычисления
print("Площадь:", result)

# Закрываем соединение
client.close()
```

### Пример выполнения:
1. Запустите сервер: `python tcp_math_server.py`
2. Запустите клиент: `python tcp_math_client.py`
3. Введите основание параллелограмма (например: `5`)
4. Введите высоту параллелограмма (например: `3`)
5. На стороне клиента отобразится: `Площадь: 15.0`

### Вывод по заданию:
Для выполнения задания 2 созданы два файла: tcp_math_server.py (сервер) и tcp_math_client.py (клиент). Серверная часть реализует TCP-сокет, который принимает соединения на порту 1235 и ожидает от клиента два числа — основание и высоту параллелограмма. Клиентская часть запрашивает у пользователя эти значения, устанавливает TCP-соединение с сервером и отправляет данные. Сервер вычисляет площадь параллелограмма по формуле S = a * h и возвращает результат клиенту. Задание выполнено успешно — реализовано клиент-серверное взаимодействие по протоколу TCP для выполнения математических вычислений.

## Задание 3

Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла index.html.

### Требования:

- Обязательно использовать библиотеку socket.

### Реализация

**Серверная часть:**

```py title="html_server.py" 
import socket

# Создаем TCP сокет
# AF_INET - используем IPv4
# SOCK_STREAM - указываем TCP протокол
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет к адресу и порту
server.bind(('localhost', 8080))

# Начинаем прослушивание соединений
server.listen(1)
print(f"Сервер запущен на http://localhost:8080")

# Загружаем HTML-страницу из файла
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

while True:
    # Принимаем соединение от клиента
    conn, addr = server.accept()
    
    # Получаем запрос от клиента
    request = conn.recv(1024).decode('utf-8')
    
    # Формируем HTTP-ответ
    response = f"""HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: {len(html.encode('utf-8'))}
Connection: close

{html}"""
    
    # Отправляем ответ клиенту
    conn.sendall(response.encode('utf-8'))
    
    # Закрываем соединение
    conn.close()
```

**Клиентская часть:**

```py title="html_client.py" 
import socket

# Создаем TCP сокет
# AF_INET - используем IPv4
# SOCK_STREAM - указываем TCP протокол
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Устанавливаем соединение с сервером
client.connect(('localhost', 8080))

# Отправляем HTTP GET-запрос
client.send(b"GET / HTTP/1.1\r\n\r\n")

# Получаем ответ от сервера
response = client.recv(4096).decode('utf-8')

# Выводим ответ
print(response)

# Закрываем соединение
client.close()
```

### Пример выполнения:
1. Убедитесь в существовании файла `index.html`
2. Запустите сервер: `python html_server.py`
3. Запустите клиент: `python html_client.py`
4. Клиент получит полный HTTP-ответ с HTML-страницей

### Вывод по заданию:
Для выполнения задания 3 созданы два файла: html_server.py (сервер) и html_client.py (клиент). Серверная часть реализует TCP-сокет, который принимает соединения на порту 8080 и прослушивает входящие HTTP-запросы. При получении GET-запроса сервер загружает HTML-страницу из файла index.html, формирует корректный HTTP-ответ с заголовками (статус 200 OK, Content-Type, Content-Length) и отправляет его клиенту. Клиентская часть устанавливает TCP-соединение с сервером, отправляет HTTP GET-запрос и получает ответ, содержащий HTML-страницу. Задание выполнено успешно — реализован простой HTTP-сервер, способный обслуживать HTML-страницы по протоколу TCP.

## Задание 4

Реализовать двухпользовательский или многопользовательский чат. Для максимального количества баллов реализуйте
многопользовательский чат.

#### Требования:

- Обязательно использовать библиотеку socket.
- Для многопользовательского чата необходимо использовать библиотеку threading.
- В практике 4 чат должен быть многопользовательским (больше двух человек) и для запуска каждого клиента должен использоваться 1 файл (грубо говоря вы 3 раза запускаете client.py и у вас коннектятся 3 юзера)
#### Реализация:

- Протокол TCP: 100% баллов.
- Для TCP запустите клиентские подключения и обработку сообщений от всех пользователей в потоках. Не забудьте сохранять
  пользователей, чтобы отправлять им сообщения.

### Реализация

**Серверная часть:**

```py title="chat_server.py" 
import socket
import threading

# Список для хранения всех подключенных клиентов
clients = []
# Блокировка для потокобезопасной работы со списком клиентов
lock = threading.Lock()


def send_to_all(msg, sender=None):
    """
    Отправляет сообщение всем подключенным клиентам, кроме отправителя
    :param msg: сообщение для отправки
    :param sender: клиент-отправитель (чтобы не отправлять ему же)
    """
    with lock:
        for client in clients:
            if client != sender:
                try:
                    client.send(msg.encode())
                except:
                    # Удаляем клиента при ошибке отправки
                    clients.remove(client)


def handle_client(client, addr):
    """
    Обрабатывает подключение одного клиента в отдельном потоке
    :param client: сокет клиента
    :param addr: адрес клиента (IP, порт)
    """
    try:
        # Получаем никнейм от клиента
        nickname = client.recv(1024).decode().strip()
        if not nickname:
            nickname = f"user_{addr[1]}"

        # Добавляем клиента в список подключенных
        with lock:
            clients.append(client)

        # Уведомляем всех о новом пользователе
        send_to_all(f"{nickname} присоединился")

        # Основной цикл получения сообщений от клиента
        while True:
            msg = client.recv(1024).decode().strip()
            # Если сообщение пустое или команда выхода - завершаем
            if not msg or msg == "/quit":
                break
            # Отправляем сообщение всем остальным клиентам
            send_to_all(f"{nickname}: {msg}", sender=client)
    except:
        # Обрабатываем любые исключения (например, разрыв соединения)
        pass
    finally:
        # Удаляем клиента из списка при завершении
        with lock:
            if client in clients:
                clients.remove(client)
        # Закрываем соединение с клиентом
        try:
            client.close()
        except:
            pass


# Создаем TCP сокет сервера
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Привязываем сокет к localhost и порту 1238
server.bind(('localhost', 1238))
# Начинаем прослушивать входящие соединения
server.listen()

print("Сервер запущен на порту 1238")

# Бесконечный цикл принятия новых подключений
while True:
    # Принимаем новое подключение
    client, addr = server.accept()
    # Запускаем обработку клиента в отдельном потоке
    threading.Thread(target=handle_client, args=(client, addr), daemon=True).start()
```

**Клиентская часть:**

```py title="chat_client.py" 
import socket
import threading


def receive_messages(sock):
    """
    Функция для получения сообщений от сервера в отдельном потоке
    :param sock: сокет клиента
    """
    while True:
        try:
            # Получаем сообщение от сервера
            msg = sock.recv(4096).decode()
            # Если сообщение пустое (сервер отключился) - выходим
            if not msg:
                break
            # Выводим полученное сообщение
            print(f"\n{msg}\n> ", end="")
        except:
            # Обрабатываем ошибки соединения
            break


# Запрашиваем никнейм у пользователя
nickname = input("Введите ник: ").strip()
if not nickname:
    nickname = "user"

# Создаем TCP сокет клиента
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Подключаемся к серверу на localhost, порт 1238
sock.connect(('localhost', 1238))

# Отправляем серверу свой никнейм
sock.send(f"{nickname}\n".encode())

# Запускаем поток для получения сообщений от сервера
threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

print("> ", end="")

# Основной цикл для отправки сообщений
while True:
    # Читаем ввод пользователя
    msg = input()
    # Если команда выхода - отправляем её серверу и выходим
    if msg.strip().lower() == "/quit":
        sock.send(b"/quit\n")
        break
    # Отправляем сообщение на сервер
    sock.send(f"{msg}\n".encode())
    print("> ", end="")

# Закрываем соединение
sock.close()
```

### Пример выполнения:
1. Запустите сервер: `python chat_server.py`
2. Запустите первый клиент: `python chat_client.py`
   - Введите ник: `user 1`
3. Запустите второй клиент: `python chat_client.py`
   - Введите ник: `user 2`
4. Запустите третий клиент: `python chat_client.py`
   - Введите ник: `user 3`
5. Все три клиента смогут обмениваться сообщениями в реальном времени

### Пример работы чата:
```
[Сервер] Сервер запущен на порту 1238

[Клиент 1] Введите ник: user 1
> 

[Клиент 2] Введите ник: user 2
> 

[Клиент 3] Введите ник: user 3
> 

[Все клиенты видят]
user 1 присоединился
user 2 присоединился
user 3 присоединился

[Клиент 1 пишет] hi i am user 1
[Клиент 2 и 3 видят] user 1: hi i am user 1

[Клиент 2 пишет] hi user 1. i am user 2 i see you!
[Клиент 1 и 3 видят] user 2: hi user 1. i am user 2 i see you!

[Клиент 3 пишет] hi you both i am user 3
[Клиент 1 и 2 видят] user 3: hi you both i am user 3
```

### Вывод по заданию:
Для выполнения задания 4 созданы два файла: chat_server.py (сервер) и chat_client.py (клиент). Серверная часть реализует многопользовательский TCP-чат, где каждое клиентское подключение обрабатывается в отдельном потоке с помощью библиотеки threading. Сервер поддерживает список всех подключенных клиентов и обеспечивает рассылку сообщений от одного пользователя всем остальным. Клиентская часть также использует многопоточность: основной поток обрабатывает ввод сообщений пользователем, а дополнительный поток — получение сообщений от сервера. Задание выполнено успешно — реализован многопользовательский чат (поддерживающий более двух участников) с использованием TCP протокола и потоковой обработки, где все клиенты используют один и тот же файл chat_client.py для подключения.


## Задание 5

Написать простой веб-сервер для обработки GET и POST HTTP-запросов с помощью библиотеки socket в Python.

#### Сервер должен:

- Принять и записать информацию о дисциплине и оценке по дисциплине.
- Отдать информацию обо всех оценках по дисциплинам в виде HTML-страницы.
- В практике 5 вы создаёте журнал. Это значит что как минимум необходимо структурировано хранить оценки по каждому добавленному предмету (условно добавив 2 оценки к дисциплине "Математика" вы должны в результате получить одну строчку с предметам со списком из двух оценок)

### Реализация

=== "Объяснение кода"

    1. **`serve_forever()`** - основной цикл сервера, принимает входящие соединения
    2. **`serve_client(conn)`** - обрабатывает каждое клиентское подключение
    3. **`parse_request(conn)`** - разбирает HTTP запрос на метод, URL, версию и заголовки
    4. **`parse_headers(rfile)`** - читает все заголовки HTTP запроса
    5. **`handle_request(req)`** - определяет, какой обработчик вызвать в зависимости от метода и пути
    6. **`send_response(conn, resp)`** - формирует и отправляет HTTP ответ клиенту

    1. **Структурированное хранение данных:** Используется словарь `self._grades`, где ключ - название дисциплины, значение - список оценок. Это позволяет хранить несколько оценок по одной дисциплине.
    2. **Поддержка GET и POST:** Сервер обрабатывает оба типа запросов:
    - **GET `/`** - отображает главную страницу с формой и таблицей оценок
    - **POST `/add`** - принимает данные из формы и добавляет новую оценку
    3. **Валидация данных:** Проверяется корректность введенных данных:
      - Оценка должна быть числом от 1 до 5
      - Поля "дисциплина" и "оценка" обязательны
    4. **Динамическая генерация HTML:** Сервер загружает шаблон `index.html` и заменяет placeholder `<!--GRADES_TABLE-->` на сгенерированную таблицу с оценками.
    5. **Перенаправление после добавления:** После успешного добавления оценки сервер отправляет код 303 (See Other) с заголовком Location, что вызывает перезагрузку страницы.
    6. **Корректная обработка кодировок:** 
      - Заголовки обрабатываются в кодировке ISO-8859-1 (как требует HTTP стандарт)
      - Тело запроса и ответа - в UTF-8 для поддержки кириллицы
      - URL-encoded параметры декодируются с помощью `unquote()`


=== "server.py"

    ```py title="server.py" 
    import socket
    import sys
    from urllib.parse import unquote
    
    
    class MyHTTPServer:
        # Параметры сервера
        def __init__(self, host, port, server_name):
            self._host = host
            self._port = port
            self._server_name = server_name
            # Хранилище оценок: {дисциплина: [оценки]}
            self._grades = {}
    
        def serve_forever(self):
            # 1. Запуск сервера на сокете, обработка входящих соединений
            serv_sock = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM,
                proto=0)
    
            try:
                serv_sock.bind((self._host, self._port))
                serv_sock.listen()
    
                print(f"Сервер запущен на http://{self._host}:{self._port}")
    
                while True:
                    conn, _ = serv_sock.accept()
                    try:
                        self.serve_client(conn)
                    except Exception as e:
                        print(f'Ошибка при обработке клиента: {e}')
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
                self.send_error(conn, e)
    
            if conn:
                conn.close()
    
        def parse_request(self, conn):
            # 3. функция для обработки заголовка http+запроса. Python, сокет предоставляет возможность создать вокруг него некоторую обертку, которая предоставляет file object интерфейс. Это дайте возможность построчно обработать запрос. Заголовок всегда - первая строка. Первую строку нужно разбить на 3 элемента  (метод + url + версия протокола). URL необходимо разбить на адрес и параметры (isu.ifmo.ru/pls/apex/f?p=2143 , где isu.ifmo.ru/pls/apex/f, а p=2143 - параметр p со значением 2143)
            rfile = conn.makefile('rb')
    
            line = rfile.readline(65537)
            if len(line) > 65536:
                raise Exception('Request line is too long')
    
            req_line = line.decode('iso-8859-1')
            req_line = req_line.rstrip('\r\n')
    
            words = req_line.split()
            if len(words) != 3:
                raise Exception('Malformed request line')
    
            method, target, ver = words
    
            if ver != 'HTTP/1.1':
                raise Exception('Unexpected HTTP version')
    
            headers = self.parse_headers(rfile)
    
            # Читаем тело запроса для POST
            body = None
            if method == 'POST':
                content_length = headers.get('Content-Length')
                if content_length:
                    try:
                        body_length = int(content_length)
                        body = rfile.read(body_length).decode('utf-8')
                    except:
                        pass
    
            host = headers.get('Host')
            if not host:
                raise Exception('Host header is missing')
    
            return {
                'method': method,
                'target': target,
                'version': ver,
                'headers': headers,
                'body': body
            }
    
        def parse_headers(self, rfile):
            # 4. Функция для обработки headers. Необходимо прочитать все заголовки после первой строки до появления пустой строки и сохранить их в массив.
            headers = {}
    
            while True:
                line = rfile.readline(65537)
                if len(line) > 65536:
                    raise Exception('Header line is too long')
    
                if line in (b'\r\n', b'\n', b''):
                    break
    
                header_line = line.decode('iso-8859-1').rstrip('\r\n')
                if ': ' in header_line:
                    key, value = header_line.split(': ', 1)
                    headers[key] = value
    
            return headers
    
        def handle_request(self, req):
            # 5. Функция для обработки url в соответствии с нужным методом. В случае данной работы, нужно будет создать набор условий, который обрабатывает GET или POST запрос. GET запрос должен возвращать данные. POST запрос должен записывать данные на основе переданных параметров.
            method = req['method']
            target = req['target']
            body = req.get('body')
    
            # Разбираем параметры
            params = {}
    
            if method == 'GET':
                # GET параметры из URL
                if '?' in target:
                    path, query_string = target.split('?', 1)
                else:
                    path = target
                    query_string = ''
    
                if query_string:
                    for param in query_string.split('&'):
                        if '=' in param:
                            key, value = param.split('=', 1)
                            params[unquote(key)] = unquote(value)
            elif method == 'POST':
                # POST параметры из тела запроса
                path = target
                if body:
                    for param in body.split('&'):
                        if '=' in param:
                            key, value = param.split('=', 1)
                            params[unquote(key)] = unquote(value)
            else:
                path = target
    
            # Обработка запросов
            if path == '/' and method == 'GET':
                return self.handle_get_grades()
    
            if path == '/add' and (method == 'GET' or method == 'POST'):
                return self.handle_add_grade(params)
    
            return self.error_response(404, 'Not Found')
    
        def handle_get_grades(self):
            # Загружаем HTML шаблон
            with open('index.html', 'r', encoding='utf-8') as f:
                html_template = f.read()
    
            # Генерируем таблицу с оценками
            grades_table = self.generate_grades_table()
    
            # Заменяем placeholder в шаблоне
            html = html_template.replace('<!--GRADES_TABLE-->', grades_table)
    
            headers = [
                ('Content-Type', 'text/html; charset=utf-8'),
                ('Content-Length', str(len(html.encode('utf-8'))))
            ]
    
            return {'status': 200, 'reason': 'OK', 'headers': headers, 'body': html}
    
        def handle_add_grade(self, params):
            if 'discipline' not in params or 'grade' not in params:
                return self.error_response(400, 'Bad Request', 'Missing discipline or grade parameter')
    
            discipline = params['discipline']
            grade = params['grade']
    
            if not grade.isdigit():
                return self.error_response(400, 'Bad Request', 'Grade must be a number')
    
            grade = int(grade)
    
            if grade < 1 or grade > 5:
                return self.error_response(400, 'Bad Request', 'Grade must be between 1 and 5')
    
            if discipline not in self._grades:
                self._grades[discipline] = []
    
            self._grades[discipline].append(grade)
    
            headers = [('Location', '/')]
            return {'status': 303, 'reason': 'See Other', 'headers': headers, 'body': ''}
    
        def send_response(self, conn, resp):
            # 6. Функция для отправки ответа. Необходимо записать в соединение status line вида HTTP/1.1 <status_code> <reason>. Затем, построчно записать заголовки и пустую строку, обозначающую конец секции заголовков.
            wfile = conn.makefile('wb')
    
            status_line = f"HTTP/1.1 {resp['status']} {resp['reason']}\r\n"
            wfile.write(status_line.encode('iso-8859-1'))
    
            if 'headers' in resp:
                for key, value in resp['headers']:
                    header_line = f"{key}: {value}\r\n"
                    wfile.write(header_line.encode('iso-8859-1'))
    
            wfile.write(b'\r\n')
    
            if 'body' in resp and resp['body']:
                wfile.write(resp['body'].encode('utf-8'))
    
            wfile.flush()
            wfile.close()
    
        def send_error(self, conn, err):
            error_msg = str(err)
            body = error_msg.encode('utf-8')
    
            headers = [
                ('Content-Type', 'text/plain; charset=utf-8'),
                ('Content-Length', str(len(body)))
            ]
    
            resp = {'status': 500, 'reason': 'Internal Server Error', 'headers': headers, 'body': error_msg}
            self.send_response(conn, resp)
    
        def error_response(self, status, reason, body=None):
            if body is None:
                body = reason
    
            body_encoded = body.encode('utf-8')
            headers = [
                ('Content-Type', 'text/plain; charset=utf-8'),
                ('Content-Length', str(len(body_encoded)))
            ]
    
            return {'status': status, 'reason': reason, 'headers': headers, 'body': body}
    
        def generate_grades_table(self):
            if not self._grades:
                return '<p>Нет оценок. Добавьте первую оценку!</p>'
    
            table_html = '''
        <table>
            <tr>
                <th>Дисциплина</th>
                <th>Оценки</th>
            </tr>'''
    
            for discipline, grades in sorted(self._grades.items()):
                grades_str = ', '.join(map(str, grades))
    
                table_html += f'''
            <tr>
                <td>{discipline}</td>
                <td>{grades_str}</td>
            </tr>'''
    
            table_html += '''
        </table>'''
    
            return table_html
    
    
    if __name__ == '__main__':
        host = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 8080
        name = sys.argv[3] if len(sys.argv) > 3 else 'localhost'
    
        serv = MyHTTPServer(host, port, name)
        try:
            serv.serve_forever()
        except KeyboardInterrupt:
            pass
    ```

=== "HTML шаблон"

    ```html title="index.html"
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Журнал оценок</title>
        <style>
            body { font-family: Arial; margin: 20px; }
            table { border-collapse: collapse; margin: 20px 0; }
            th, td { border: 1px solid #ddd; padding: 8px; }
            th { background-color: #f2f2f2; }
            form { margin: 20px 0; }
            input, button { padding: 5px; margin: 2px; }
        </style>
    </head>
    <body>
        <h1>Журнал оценок</h1>
    
        <form action="/add" method="POST">
            <input type="text" name="discipline" placeholder="Дисциплина" required>
            <input type="number" name="grade" placeholder="Оценка (1-5)" min="1" max="5" required>
            <button type="submit">Добавить</button>
        </form>
    
        <h2>Оценки:</h2>
    
        <!--GRADES_TABLE-->
    
    </body>
    </html>
    ```

### Пример выполнения:
1. Запуск сервера: `python server.py`
2. Открыть в браузере: `http://localhost:8080/`
3. Добавить дисциплину и оценку 
4. Оценки по дисциплинам отображаются в таблице

### Вывод по заданию:
Для выполнения задания 5 создан файл `server.py`, реализующий класс `MyHTTPServer` по заданной структуре (Полезные ссылки: Базовый класс для веб-сервера). Сервер корректно обрабатывает GET и POST HTTP-запросы, принимает информацию о дисциплине и оценке, сохраняет ее в структурированном виде (словарь: ключ - дисциплина, значение - список оценок) и отображает все оценки в виде HTML-страницы. При добавлении нескольких оценок по одной дисциплине они группируются в одну строку таблицы. Сервер реализует все шесть требуемых методов: `serve_forever()`, `serve_client()`, `parse_request()`, `parse_headers()`, `handle_request()` и `send_response()`. Задание выполнено успешно — создан полнофункциональный веб-сервер для ведения журнала оценок с поддержкой HTTP протокола.