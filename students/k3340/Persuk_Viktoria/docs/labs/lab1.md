## Сокеты

**Сокет** - некоторая абстракция ОС, специальный программный интерфейс, который позволяем программам обмениваться данными между собой. Различают серверные и клиентские сокеты.

**Серверный сокет**:

- Устанавливает адрес и порт сокета (`bind()`)
- Слушает соединения (`listen()`)
- Принимает клиентов (`accept()`)
- Отправляет и принимает сообщения от клиента (`send`, `recv`)

**Клиентский сокет**:

- Подключается к серверному сокету (`connect()`)
- Отправляет и принимает сообщения от сервера (`send`, `recv`)

Сокеты могут ещё иметь разную *конфигурацию*: использовать IPv4 или IPv6, работать поверх TCP или UDP, иметь разный тип передачи данных - потоковыый или датаграммный.

## Чуть про UDP vs TCP

#### UDP протокол

UDP протокол работает довольно быстро, но целостность данных не гарантируется. Для UDP не надо устанавливать соединения, можно сразу начинать отправлять пакеты данных

Данные отправляются датаграммами (данные дробятся на более мелкие пакеты) и отправляются с сервера сплошным потоком, не ожидая фидбека от клиента

Используется для стримминга видео и аудио, VoIP, онлайн-игр

#### TCP протокол

TCP более безопасный и надёжный протокол потоковой передачи данных, так как он:

- устанавливает соединение между сервером и клиентом
- проверяет все ли данные доставились
- сохраняет порядок отправленных данных

По факту на payload навешиваются служебные пакеты - IP headers и TCP headers, это позволяет однозначно установить соединение. Чаще всего используется для веб-страниц, загрузки файлов и прочее

!!! info "NB:"
    Почти в каждом задании реализован отдельно код для сервера (`server.py`) и клиента (`client.py`)


!!! info "NB:"
    Важно отметить ещё то, что все сообщения, которые отправляются через сокет, должны быть закодированы в байты (метод `.encode()`), а при получении сообщения - декодированы (метод `.decode()`)

## Задание 1 - Работа с UDP протоколом

Ничего сложного, пишем для серверной части функцию запуска сервера с открытием сокета с `type = socket.SOCK_DGRAM` (UDP протокол). Дальше сервер открывает сокет на указанных хосте и порту (`bind()`), получает и отправляет сообщения.

Листинг кода для `server.py`:

```python
import socket


def run_server(host: str = '127.0.0.1', port: int = 8080) -> None:
    '''
    Запуск UDP-сервера
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind((host, port))
        print(f'Server started at {host}:{port}')

        data, client_addr = server.recvfrom(1024)
        print(f'Recieved message from client: {data.decode()}')

        msg = 'Hello, client'
        server.sendto(msg.encode(), client_addr)
        print(f'Sended message to client {client_addr[0]}:{client_addr[1]}: {msg}')

if __name__ == '__main__':
    run_server()
```

Для клиента тоже пишем функцию для запуска клиента собственно, подключаемся к хосту и порту сервера, получаем и отправляем сообщения.

Листинг кода для `client.py`:

```python
import socket


def run_client(server_host: str = '127.0.0.1', server_port: int = 8080):
    '''
    Запуск клиента и подключение с UDP-серверу
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
        msg = 'Hello, server'

        client.sendto(msg.encode(), (server_host, server_port))
        print(f'Message send to server {server_host}:{server_port}: {msg}')

        data, _ = client.recvfrom(1024)
        print(f'Recieced response from server: {data.decode()}')


if __name__ == '__main__':
    run_client()
```

При запуске в терминале сначала сервера, потом клиента, сначала на сервере увидим сообщение "Hello, server", потом сервер ответит на это сообщением "Hello, client". Ну и заодно будут видны логи кто что кому отправил.

## Задание 2 - Работа с TCP протоколом

Во втором задании требовалось создать сокет на TCP, где сервер запрашивает какую-либо инфу у клиента, получает её, обрабатывает и отправляет клиенту ответ

У меня 1 вариант, поэтому операция теорема Пифагора. Ничего сложного, но допустимы разные варианты использования теоремы Пифагора - по катетам найти гипотенузу, по катету и гипотенузе найти оставшийся катет и проверить выполнение (или невыполнение) теоремы Пифагора, если даны все 3 переменные.

Я написала функцию для этой операции:

```python
from math import sqrt
from typing import Tuple


def calculate_pythagorean(
        a: float | None = None,
        b: float | None = None,
        c: float | None = None
        ) -> Tuple[float, float] | bool:
    '''
    Подсчёт значений катетов/гипотенузы по теореме Пифагора
    с переменным количеством переменных (минимум 2 не None)
    '''
    count_arguments = sum(x is None for x in (a, b, c))
    if count_arguments >= 2:
        raise ValueError('Должно быть передано как минимум 2 аргумента')

    # 3 случая рассматриваем
    if (a is not None) and (b is not None) and (c is None):
        # даны только a и b
        c = sqrt(a ** 2 + b ** 2)
        c_squared = c ** 2
        return ((c_squared, c))

    elif ((a is not None) and (b is None) and (c is not None)) or \
        ((a is None) and (b is not None) and (c is not None)):
        # даны только a и c
        if b is None:
            b = a

        a = round(sqrt(c ** 2 - b ** 2), 2)
        a_squared = round(a ** 2, 2)
        return ((a_squared, a))

    else:
        # даны a, b и c
        return True if ((a ** 2 + b ** 2) == (c ** 2)) else False
```

Далее идёт работа с сервером и клиентом. Сервер уже открывает сокет с другим типом подключения `type = socket.SOCK_STREAM`, что означает TCP протокол и проделывает цепочку действий: `bind() -> listen() -> accept()`.

После подключения клиента, сервер ждёт данные от него (которые пользвователь интерактивно вводит с клавиатуры), проверяет, что данные реально есть, отправляет их в функцию `calculate_pythagorean`, получает из неё результат и отправляет обратно клиенту.

Листинг кода `server.py`:

```python
import socket


def run_server(server_host: str = '127.0.0.1', server_port: int = 8080):
    '''Запуск TCP-сервера'''

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((server_host, server_port))
        server.listen(1)
        print(f'Сервер слушает на {server_host}:{server_port}')
        conn, addr = server.accept()

        with conn:
            print(f'Подключено клиентом {addr}')
            data = conn.recv(1024)

            if data:
                params = data.decode().split(',')
                a, b, c = [int(x) if x else None for x in params]

                try:
                    result = calculate_pythagorean(a, b, c)
                except Exception as e:
                    conn.sendall(f'Ошибка: {e}'.encode())
                else:
                    conn.sendall(str(result).encode())


if __name__ == '__main__':
    run_server()
```

Клиент же подключается к серверу с указанным хостом и портом, ждёт от пользователя ввода данных с клавиатуры, отправляет полученные от пользователя данные серверу, получает ответ от пользователя.

Листинг кода `client.py`:

```python
import socket


def run_client(server_host: str = '127.0.0.1', server_port: int = 8080):
    '''
    Запуск клиента и подключение к TCP серверу
    '''

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((server_host, server_port))

        a = input('Значение катета a (или пусто): ')
        b = input('Значение катета b (или пусто): ')
        c = input('Значение гипотенузы c (или пусто): ')

        params = ','.join([a, b, c])
        client.sendall(params.encode())

        data = client.recv(1024)
        print(f'Результат от сервера: {data.decode()}')


if __name__ == '__main__':
    run_client()
```

## Задание 3 - HTTP-сервер

В третьем задании требовалось реализовать простой HTTP-сервер на сокетах. Клиент подключается к серверу, отправляет HTTP-запрос, а сервер в ответ возвращает корректное HTTP-сообщение с заголовками и HTML-страницей. Сервер работает поверх TCP (`socket.SOCK_STREAM`), так как HTTP-протокол основан именно на нём

Сначала опять идёт алгоритм `bind() -> listen() -> accept()`. Потом сервер считывает запрос клиента через `recv()`, подгружает HTML-страничку из документа `index.html`, формирует корректный HTTP-ответ (строка статуса, заголовки (Content-Type, Content-Length и др.), разделитель \r\n\r\n и тело ответа) и отдаёт HTTP-ответ `200 OK` (если реально всё ок, соединение установлено и файл найден). Если произошла ошибка, то отправляет ошибка `404 Not Found`

Листинг кода `server.py`:

```python
import socket


def run_server(server_host: str = 'localhost', server_port: int = 8080):
    '''
    Простой TCP-сервер, который отправляет HTML-страницу по запросу от клиента
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((server_host, server_port))
        server.listen(1)
        print(f'Сервер запущен на {server_host}:{server_port}')

        conn, addr = server.accept()

        with conn:
            print(f'Подключён клиент {addr}')

            # читаем запрос от клиента
            data = conn.recv(1024)
            print(f'Получены данные от клиента: {data}')

            # загрузка HTML страницы
            try:
                with open('./index.html', encoding='utf-8') as html_page:
                    html_data = html_page.read()

                html_bytes = html_data.encode('utf-8')
                content_length = len(html_bytes)

                # собираем HTTP-ответ с HTML-контентом
                http_response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/html; charset=UTF-8\r\n"
                    f"Content-Length: {content_length}\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                )

                # отправляем клиенту HTML страничку
                conn.sendall(http_response.encode() + html_bytes)

            except FileNotFoundError:
                error_message = "<html><body><h1>404 Not Found</h1><p>Файл не найден</p></body></html>"

                error_bytes = error_message.encode('utf-8')
                content_length = len(error_bytes)

                http_response = (
                    "HTTP/1.1 404 Not Found\r\n"
                    "Content-Type: text/html; charset=UTF-8\r\n"
                    f"Content-Length: {content_length}\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                )

                conn.sendall(http_response.encode('utf-8') + error_bytes)


if __name__ == "__main__":
    run_server()
```

HTML-страница (`index.html`), которую сервер отдаёт клиенту:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Сокет на Python</title>
</head>
<body>
    <h1>Интересно, интересно</h1>
    <p>Посмотрим, что из этого выйдет</p>
</body>
</html>
```

При запуске сервера и открытии в браузере адреса `http://localhost:8080/` клиент отправляет GET-запрос, сервер его принимает и возвращает HTML-контент

Пример GET-запроса от браузера:

```
GET / HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\nsec-ch-ua: "Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"\r\nsec-ch-ua-mobile: ?0\r\nsec-ch-ua-platform: "macOS"\r\nUpgrade-Insecure-Requests: 1\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7\r\nSec-Fetch-Site: none\r\nSec-Fetch-Mode: navigate\r\nSec-Fetch-User: ?1\r\nSec-Fetch-Dest: document\r\nAccept-Encoding: gzip, deflate, br, zstd\r\nAccept-Language: en-GB,en-US;q=0.9,en;q=0.8,ru;q=0 7\r\n\r\n
```

В итоге в браузере будет отображена страница с заголовком и текстом из `index.html`. Если файл отсутствует, браузер вместо страницы получит сообщение о 404 Not Found

## Задание 4 - Многопользовательский чат с потоками

Я реализовала многопользовательский чат на протоколе TCP с использованием библиотеки `threading`

Сервер хранит всех подключённых пользователей в общем словаре, где ключом является сокет, а значением — никнейм пользователя. Для корректной работы с разделяемым ресурсом (списком клиентов) используется блокировка (`threading.Lock`), чтобы избежать race condition. Алгоритм работы следующий: сервер запускается и начинает слушать входящие соединения, при подключении нового клиента создаётся поток, где происходит регистрация пользователя (никнейм отправляется на сервер первым сообщением), затем запускается цикл приёма сообщений. Каждое сообщение от клиента сервер рассылает всем остальным пользователям через функцию `broadcast`. Если пользователь отключается или его соединение обрывается, сервер удаляет его из списка активных клиентов и уведомляет остальных о выходе из чата

Листинг кода `server.py`:

```python
import socket
import threading
from typing import Tuple, Dict


# клиент == пользователь

# Храним подключённые сокеты (пользователей)
clients: Dict[socket.socket, str] = {} # сокет: никнейм
# блокировка, чтобы не было race condition
clients_lock = threading.Lock()


def broadcast(message: str) -> None:
    '''
    Отправляет сообщение всем пользователям
    message: сообщение в байтах
    sender_socket: сокет, откуда пришло сообщение
    '''
    with clients_lock:
        for client in list(clients):
            # Отправляем сообщение всем
            try:
                client.send(message.encode('utf-8'))
            except Exception:
                # Предполагаем, что если невозможно отправить пользователю сообщение,
                # то он отключился от сервера, удаляем его сокет
                client.close()
                del clients[client]


def handle_client(client_socket: socket.socket, client_address: Tuple[str, int]) -> None:
    '''
    Обработчик для каждого пользователям в отдельном потоке
    Получает сообщение от пользователям и рассылает всем остальным пользователям
    client_socket: клиентский сокет
    client_address: пара (IP, порт)
    '''
    nickname = client_socket.recv(1024).decode('utf-8').strip()
    # Добавили нового пользователя в список подключённых пользователей
    with clients_lock:
        clients[client_socket] = nickname
    print(f'[Сервер]: {nickname} присоединился к чату')

    while True:
        try:
            msg = client_socket.recv(1024)
            if not msg:
                print(f'Пользователь [{client_address}/{nickname}] отключился от чата')
                broadcast(f'[Сервер]: {nickname} покинул чат')
                break

            message_text = msg.decode('utf-8')
            # Вывод сообщение в консоль сервера
            print(f'{nickname}: {message_text}')

            # Отправляем сообщение всем остальным клиентам
            broadcast(f'{nickname}: {message_text}')

        except ConnectionResetError:
            # Если соединение было оборвано
            print(f'{client_address} вылетел')
            break
        except Exception as e:
            print(f'Ошибка при работе с {client_address}: {e}')

    # После выхода из цикла завершаем удаляем пользователя из списка и
    # заверщаем сессию пользователя
    with clients_lock:
        if client_socket in clients:
            del clients[client_socket]
    client_socket.close()


def run_server(server_host: str = 'localhost', server_port: int = 8080) -> None:
    '''
    Запускает сервер чата
    host: IP-адрес для привязки сервера
    port: порт для прослушивания
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((server_host, server_port))
        server.listen(5)
        print(f'Сервер чата запущен на {server_host}:{server_port}')

        while True:
            client_socket, client_address = server.accept()

            # Запускаем поток
            thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address),
                daemon=True
            )
            thread.start()


if __name__ == '__main__':
    run_server()
```

Клиент подключается к серверу, сначала отправляет свой никнейм, после чего запускается два процесса: в отдельном потоке работает функция `receive_message`, которая постоянно слушает сервер и выводит полученные сообщения на экран, а в основном потоке пользователь может вводить сообщения и отправлять их на сервер. Если пользователь вводит команду `/exit`, он выходит из чата, разрывая соединение

Листинг кода `client.py`:

```python
import threading
import socket


def receive_message(client: socket.socket) -> None:
    '''
    Постоянно ждёт и получает сообщения от сервера
    Выводит сообщения пользователю
    Запускается в отдельном потоке
    client: клиентский сокет
    '''
    while True:
        try:
            msg = client.recv(1024)
            if not msg:
                print('Соединение с сервером разорвано')
                break
            print(f'{msg.decode("utf-8")}')
        except Exception:
            print('Ошибка при приёме сообщений')
            break


def run_client(server_host: str = 'localhost', server_port: int = 8080) -> None:
    '''
    Запуск клиента и подключение к многопользовательскому чату
    server_host: IP сервера
    server_port: порт сервера
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((server_host, server_port))
        print(f'Подключено к серверу {server_host}:{server_port}')

        # Присвоение и отправка на сервер ника пользователя
        nickname = input('Введите ваш никнейм: ')
        client.send(nickname.encode('utf-8'))

        # Запускаем отдельный поток для приёма сообщений от сервера
        threading.Thread(
            target=receive_message,
            args=(client,),
            daemon=True
        ).start()

        # Цикл для отправки сообщений на сервер в основном потоке
        while True:
            msg = input('>>> ')
            if msg.lower() == '/exit':
                # Выход из чата
                print('Выход из чата')
                break

            try:
                client.send(msg.encode('utf-8'))
            except Exception:
                print('Ошибка при отправке сообщения')
                break


if __name__ == '__main__':
    run_client()
```

В итоге при запуске сервера и нескольких клиентов создаётся общий чат, где все сообщения каждого участника транслируются всем остальным. Сервер отображает лог подключений, отключений и сообщений, а клиенты могут свободно обмениваться текстовыми данными между собой

## Задание 5 - CRUD HTTP-сервер

В данной работе реализован простой HTTP-сервер на основе библиотеки `socket` в Python, который умеет принимать и обрабатывать GET и POST запросы. Основная цель программы — сохранить и отдать информацию об оценках по дисциплинам. Для удобства и читаемости кода выделены два класса: `Request` и `MyHTTPServer`

Начнём с класса `Request`. Его назначение — хранить все данные о запросе в одном месте. Когда клиент отправляет запрос, должен быть доступ к методу, к пути, к параметрам, к версии протокола, к заголовкам и, при необходимости, к телу запроса. Всё это аккуратно упаковывается в объект `Request`, чтобы потом сервер мог с ним работать.

Конструктор этого класса выглядит так:

```python
class Request:
    def __init__(self,
                 method: str,
                 addr: str,
                 param: str,
                 version_proto: str,
                 headers: Optional[Dict[str, str]] = None,
                 body: str = '') -> None:
        self.method = method
        self.addr = addr
        self.param = param
        self.version_proto = version_proto
        self.headers = headers or {}
        self.body = body
```

Главная логика сосредоточена в классе `MyHTTPServer`. Именно он запускает сокет, принимает соединения, парсит запросы и отправляет клиенту ответы. При создании экземпляра этого класса указываются адрес и порт, а также инициализируется словарь `grades`, где будут храниться пары «дисциплина — оценка»

Запуск сервера происходит в методе `serve_forever`. Здесь создаётся TCP-сокет, который привязывается к указанному адресу, начинает слушать соединения и в бесконечном цикле принимает клиентов. После подключения клиента управление передаётся методу `serve_client`

Сам код выглядит так:

```python
def serve_forever(self) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((self._host, self._port))
        server.listen(1)
        print(f'Сервер слушает на {self._host}:{self._port}')

        while True:
            conn, _ = server.accept()
            try:
                self.serve_client(conn)
            except Exception as e:
                print(f'Ошибка клиента: {e}')
            finally:
                conn.close()
```

Метод `serve_client` принимает подключение и обрабатывает запрос. Здесь последовательно вызываются вспомогательные методы для разбора запроса. Сначала `parse_request` считывает первую строку (например, `GET /grades HTTP/1.1`), выделяет метод, путь, параметры и версию протокола и возвращает объект `Request`. Затем вызывается `parse_headers`, который построчно считывает заголовки и формирует словарь. Если в заголовках указан `Content-Length`, то сервер понимает, что запрос содержит тело (актуально для POST), и считывает ровно указанное количество байт. После этого полностью готовый объект запроса передаётся в `handle_request`

Пример кода для разбора заголовков:

```python
def parse_headers(self, stream) -> Dict[str, str]:
    headers = {}
    while True:
        line = stream.readline().decode('utf-8').strip()
        if not line:
            break
        if ': ' in line:
            header, value = line.split(': ')
            headers[header] = value
    return headers
```

В методе `handle_request` сосредоточена бизнес-логика. Если приходит GET-запрос на адрес `/grades`, сервер возвращает HTML-страницу с таблицей оценок. Если приходит POST-запрос на тот же адрес, сервер ожидает данные формы с ключами `subject` и `grade`. В случае успешного получения данных они сохраняются в словарь `grades`, после чего клиенту возвращается обновлённая таблица. Если же данные отсутствуют, сервер отвечает ошибкой 400

Часть логики метода выглядит так:

```python
if req.method == 'POST' and req.addr == '/grades':
    form = parse_qs(req.body)
    subject = form.get('subject', [''])[0]
    grade = form.get('grade', [''])[0]

    if subject and grade:
        self.grades[subject] = grade
        response_html = self._render_grades_page()
        self.send_response(conn, 200, 'OK', response_html)
    else:
        self.send_response(conn, 400, 'Bad Request',
                           '<h2>Ошибка: не заданы subject или grade</h2>')
```

Для формирования ответа клиенту используется метод `send_response`. Он собирает строку статуса (например, `HTTP/1.1 200 OK`), добавляет заголовки (тип содержимого, длина ответа) и соединяет их с телом HTML-страницы. Всё это переводится в байты и отправляется через сокет

HTML-страница с оценками формируется во вспомогательном методе `_render_grades_page`. В нём перебираются все пары «дисциплина — оценка» из словаря, создаются строки таблицы, которые вставляются внутрь шаблона. В результате клиент получает полноценную HTML-страницу с заголовком и таблицей

```python
def _render_grades_page(self) -> str:
    rows = ''.join(
        f'<tr><td>{discipline}</td><td>{grade}</td></tr>'
        for discipline, grade in self.grades.items()
    )
    html = f"""
    <html>
        <head>
            <title>Оценки по дисциплинам</title>
        </head>
        <body>
            <h1>Оценки студентов</h1>
            <table border="1" cellpadding="5" cellspacing="0">
                <tr>
                    <th>Дисциплина</th>
                    <th>Оценка</th>
                </tr>
                {rows}
            </table>
        </body>
    </html>
    """
    return html
```

В блоке `if __name__ == '__main__':` создаётся объект сервера с указанным адресом и портом, после чего запускается метод `serve_forever`, программа будет работать до тех пор, пока её не остановить вручную

Полный листинг кода:

```python
import socket
from typing import Dict, Optional
from urllib.parse import parse_qs


class Request:
    '''
    Класс для хранения данных HTTP-запросов

    Атрибуты:
        method (str): HTTP-метод запроса ('GET', 'POST', ...)
        addr (str): путь или ресурс из URL без параметров запроса
        param (str): параметры запроса в URL после знака '?'
        version_proto (str): версия протокола HTTP запроса
        headers (Optional[Dict[str, str]]): словарь HTTP-заголовков, где ключ — имя заголовка, а значение — соответствующее ему значение
        body (str): тело HTTP-запроса (текстовое содержимое)
    '''
    def __init__(self,
                 method: str,
                 addr: str,
                 param: str,
                 version_proto: str,
                 headers: Optional[Dict[str, str]] = None,
                 body: str = '') -> None:
        self.method = method
        self.addr = addr
        self.param = param
        self.version_proto = version_proto
        self.headers = headers or {}
        self.body = body


class MyHTTPServer:
    '''
    Класс HTTP-сервера на основе сокетов
    '''
    def __init__(self, host: str, port: int, server_name: Optional[str] = None) -> None:
        self._host = host
        self._port = port
        self._server_name = server_name

        # хранит оценки по дисциплинам
        self.grades: Dict[str, str] = {}  # {дисциплина: оценка}


    def serve_forever(self) -> None:
        '''
        Запуск сервера на сокете, слушает и обрабатывает входящие соединения
        '''
        # Запускаем новый сокет
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((self._host, self._port))
            server.listen(1) # Работает одновременно только с одним подключением
            print(f'Сервер слушает на {self._host}:{self._port}')

            # Запускаем бесконечное прослушивание подключённого клиента
            while True:
                conn, _ = server.accept()
                try:
                    self.serve_client(conn)
                except Exception as e:
                    print(f'Ошибка клиента: {e}')
                finally:
                    conn.close()  # закрываем соединение после обработки запроса


    def serve_client(self, conn: socket.socket) -> None:
        '''
        Обрабатывает запрос клиента, используя методы парсинга запроса и заголовков
        '''
        # файловый объект для удобного чтения в потоке
        stream = conn.makefile('rb')
        # парсим запросы и заголовки
        request = self.parse_request(stream)  # --> Request
        headers = self.parse_headers(stream)

        # тк request возвращается из метода parse_request как экземпляр класса Request, то нам доступны все его переменные
        request.headers = headers

        content_length = int(headers.get('Content-Length', '0'))
        if content_length > 0:
            # Если тело HTTP запроса есть (POST), читаем ровно content_length байт из потока
            request.body = stream.read(content_length).decode('utf-8')
        else:
            request.body = ''

        # Передаём распарсенный запрос в хэндлер бизнес-логики, он уже решит, что с запросом делать
        self.handle_request(conn, request)

    def parse_request(self, stream) -> Request:
        '''
        Парсит первую строку HTTP-запроса (request line) и возвращает
        объект Request с методом, адресом, параметрами и версией протокола
        '''
        request_line = stream.readline().decode('utf-8').strip()

        if not request_line:
            raise ValueError('Отсутствует request line')

        method, url, version_proto = request_line.split(' ')
        addr, *param = url.split('?', 1)
        # если параметры не были переданы
        param = param[0] if param else ''

        return Request(method, addr, param, version_proto)


    def parse_headers(self, stream) -> Dict[str, str]:
        '''
        Парсит HTTP-заголовки из потока до пустой строки
        '''
        # next(request_lines)  # пропускаем request line, работаем долько с заголовками

        headers = {}

        while True:
            line = stream.readline().decode('utf-8').strip()
            # останавливаем поток когда доходим до пустой строки
            if not line:
                break
            if ': ' in line:
                header, value = line.split(': ')
                headers[header] = value

        return headers


    def handle_request(self, conn: socket.socket, req: Request) -> None:
        '''
        Логика обработки HTTP-запросов (GET, POST)
        '''

        # GET /grades -- получить список всех оценок
        if req.method == 'GET' and req.addr == '/grades':
            # формируем HTML страничку и отправляем с 200 кодом
            response_html = self._render_grades_page()
            self.send_response(conn, 200, 'OK', response_html)

        # POST /grades?subject=*&grade=* -- записать новую оценку по дисциплине
        if req.method == 'POST' and req.addr == '/grades':
            # Принимаем данные из тела и обновляем оценки
            form = parse_qs(req.body)
            subject = form.get('subject', [''])[0]
            grade = form.get('grade', [''])[0]

            # Если есть и предмет, и оценка
            if subject and grade:
                # Сохраняем предмет и оценку
                self.grades[subject] = grade
                # Возвращаем HTML-страницу со всеми оценками + новая оценка
                response_html = self._render_grades_page()
                self.send_response(conn, 200, 'OK', response_html)
            else:
                # При ошибке получения дисциплины или оценки кидаем 400 ошибку
                self.send_response(conn, 400, 'Bad Request', '<h2>Ошибка: не заданы subject или grade</h2>')


    def send_response(self,
                      conn: socket.socket,
                      code: int,
                      reason: str,
                      body: str,
                      content_type: str = 'text/html; charset=utf-8') -> None:
        '''
        Функция формирует и отправляет HTTP-ответ
        '''
        response_headers = [
            f'HTTP/1.1 {code} {reason}',
            f'Content-Type: {content_type}',
            f'Content-Length: {len(body.encode("utf-8"))}',
            '',
            '',
        ]

        # Переводим заголовки и тело в байты
        header_bytes = '\r\n'.join(response_headers).encode('utf-8')
        body_bytes = body.encode('utf-8')

        # Отправка заголовков и тела
        conn.sendall(header_bytes + body_bytes)


    def _render_grades_page(self) -> str:
        '''
        Рендерит (формирует) HTML-страницу со всеми оценками
        '''
        # Формируем строки в таблице (дисциплина -- оценка)
        rows = ''.join(f'<tr><td>{discipline}</td><td>{grade}</td></tr>' for discipline, grade in self.grades.items())

        # структура HTML-страницы
        html = f"""
        <html>
            <head>
                <title>Оценки по дисциплинам</title>
            </head>
            <body>
                <h1>Оценки студентов</h1>
                <table border="1" cellpadding="5" cellspacing="0">
                    <tr>
                        <th>Дисциплина</th>
                        <th>Оценка</th>
                    </tr>
                    {rows}
                </table>
            </body>
        </html>
        """

        return html


if __name__ == '__main__':
    host = 'localhost'
    port = 8080
    name = 'Grader'
    serv = MyHTTPServer(host, port, name)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print('Сервер остановлен')
```
