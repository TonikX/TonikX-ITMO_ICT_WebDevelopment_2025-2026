# Лабораторная работа 1 по предмету Web-программирование
# Задание 1.

---

## Описание
Реализованы клиентская и серверная части приложения на Python с использованием библиотеки **socket** и протокола **UDP**.  
Клиент отправляет серверу сообщение `"Hello, server"`, которое отображается на стороне сервера.  
В ответ сервер отправляет сообщение `"Hello, client"`, и оно отображается у клиента.

## Требования
- Python 3.6+
- Стандартные библиотеки:
  - `socket`

## Структура проекта
- `server.py` — код сервера
- `client.py` — код клиента
  
## Как работает сервер
1. Сервер создаёт UDP-сокет и слушает порт `9090`.
2. Клиент создаёт UDP-сокет и отправляет строку `"Hello, server"` на адрес `localhost:9090`.
3. Сервер принимает сообщение, выводит его в консоль и отправляет обратно строку `"Hello, client"`.
4. Клиент принимает ответ и выводит его в консоль.

## Запуск сервера
### Шаг 1: Запуск сервера
Откройте терминал и выполните:
```bash
cd Task1
python server.py
```
Вывод будет таким
```
UDP сервер запущен на localhost:9090...
Ожидание сообщений от клиента...
```

### Шаг 2: Запустить клиента
В другом терминале выполните:
```bash
python client_udp.py
```


**Остановка**

Для завершения работы сервера нажмите Ctrl+C в терминале.
Клиент завершает работу автоматически после получения ответа.
## Код:

**server.py**
```python
import socket

# Параметры сервера
HOST = 'localhost'  # Адрес хоста
PORT = 9090         # Порт для работы сервера

# Создаем UDP сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Привязываем сокет к адресу и порту
server_socket.bind((HOST, PORT))
print(f"UDP сервер запущен на {HOST}:{PORT}...")
print("Ожидание сообщений от клиента...")

while True:
    try:
        # Получаем данные от клиента
        data, client_address = server_socket.recvfrom(1024)
        
        # Декодируем полученное сообщение
        message = data.decode('utf-8')
        print(f"Получено сообщение от {client_address}: {message}")
        
        # Ответ для клиента
        response = "Hello, client"
        
        # Отправляем ответ клиенту
        server_socket.sendto(response.encode('utf-8'), client_address)
        print(f"Отправлен ответ клиенту {client_address}: {response}")
        
    except KeyboardInterrupt:
        print("\nСервер остановлен пользователем")
        break
    except Exception as e:
        print(f"Ошибка: {e}")

# Закрываем сокет
server_socket.close()
print("Сервер завершил работу")

```
**client.py**
```python
import socket

HOST = 'localhost'  # Адрес сервера
PORT = 9090         # Порт сервера

# Создаем UDP сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    # Сообщение для сервера
    message = "Hello, server"
    
    # Отправляем сообщение серверу
    print(f"Отправляю сообщение серверу: {message}")
    client_socket.sendto(message.encode('utf-8'), (HOST, PORT))
    
    # Получаем ответ от сервера
    print("Ожидание ответа от сервера...")
    data, server_address = client_socket.recvfrom(1024)
    
    # Декодируем полученный ответ
    response = data.decode('utf-8')
    print(f"Получен ответ от сервера {server_address}: {response}")
    
except Exception as e:
    print(f"Ошибка: {e}")
    
finally:
    # Закрываем сокет
    client_socket.close()
    print("Клиент завершил работу")

```
---
# Задание 2.

---

## Описание
Реализованы клиентская и серверная части приложения на Python с использованием библиотеки **socket** и протокола **TCP**.  
Так как в журнале мой порядковый номер 9, я реализовывала функцию **Варианта 1**.
Клиент вводит два числа (катеты прямоугольного треугольника) и отправляет их серверу.  
Сервер обрабатывает данные и возвращает клиенту результат вычисления гипотенузы по теореме Пифагора.

Формула:
`c = sqrt(a**2 + b**2)`

## Требования
- Python 3.6+
- Стандартные библиотеки:
  - `socket`
  - `math`

## Структура проекта
- `server.py` — TCP-сервер, обрабатывающий запросы
- `client.py` — TCP-клиент для отправки данных
  
## Как работает программа

1. Сервер создаёт TCP-сокет и слушает порт `9091`.
2. Клиент подключается к серверу и вводит два числа (катеты `a` и `b`).
3. Клиент отправляет данные серверу.
4. Сервер вычисляет гипотенузу по формуле `√(a² + b²)` и отправляет результат обратно.
5. Клиент выводит результат на экран.


## Запуск сервера
### Шаг 1: Запуск сервера
Откройте терминал и выполните:
```bash
cd Task2
python3 server.py
```
Вывод будет таким
```
TCP сервер запущен на localhost:9091, ожидаем подключения...
```

### Шаг 2: Запуск клиента
В другом терминале выполните:
```bash
python3 client.py
```
Введите катеты.
Например:
```
Введите катет a: 3
Введите катет b: 4
```
### Шаг 3: Результат
* В консоли клиента:
```
Подключено к серверу localhost:9091
Отправлено на сервер: 3 4
Ответ от сервера: Гипотенуза: 5.00
Клиент завершил работу
```
* В консоли сервера:
```
Подключение от ('127.0.0.1', 49485)
Получено от клиента: 3 4
Отправлено клиенту: Гипотенуза: 5.00
Соединение с ('127.0.0.1', 49485) закрыто
```

### Остановка
Для завершения работы сервера нажмите Ctrl+C в терминале.
Клиент завершает работу автоматически после получения ответа.
## Код:

**server.py**
```python
import socket
import math

HOST = 'localhost'
PORT = 9091


def handle_client(conn, addr):
    """Обработка подключения клиента."""
    print(f"Подключение от {addr}")
    try:
        # Получаем данные от клиента
        data = conn.recv(1024).decode('utf-8')
        print(f"Получено от клиента: {data}")

        # Ожидаем, что клиент отправит два числа
        parts = data.strip().split()
        if len(parts) != 2:
            response = "Ошибка: введите два числа (катеты a и b)"
        else:
            a, b = map(float, parts)
            c = math.sqrt(a ** 2 + b ** 2)
            response = f"Гипотенуза: {c:.2f}"

        # Отправляем результат клиенту
        conn.sendall(response.encode('utf-8'))
        print(f"Отправлено клиенту: {response}")

    except Exception as e:
        print(f"Ошибка при обработке клиента {addr}: {e}")
    finally:
        conn.close()
        print(f"Соединение с {addr} закрыто")


def start_server():
    """Запуск TCP-сервера для вычисления гипотенузы."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"TCP сервер запущен на {HOST}:{PORT}, ожидаем подключения...")

    try:
        while True:
            conn, addr = server_socket.accept()
            handle_client(conn, addr)
    except KeyboardInterrupt:
        print("\nСервер остановлен пользователем")
    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server()

```
**client.py**
```python
import socket

HOST = 'localhost'
PORT = 9091


def run_client():
    # Создаём TCP-сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Подключаемся к серверу
        client_socket.connect((HOST, PORT))
        print(f"Подключено к серверу {HOST}:{PORT}")

        # Ввод катетов
        a = input("Введите катет a: ")
        b = input("Введите катет b: ")

        # Отправляем данные серверу
        message = f"{a} {b}"
        client_socket.sendall(message.encode('utf-8'))
        print(f"Отправлено на сервер: {message}")

        # Получаем ответ
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Ответ от сервера: {response}")

    except Exception as e:
        print(f"Ошибка клиента: {e}")
    finally:
        client_socket.close()
        print("Клиент завершил работу")


if __name__ == "__main__":
    run_client()

```
---
# Задание 3.

---

## Описание
Реализована серверная часть приложения на Python.  
Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу `index.html`.

## Требования
- Python 3.6+
- Стандартные библиотеки:
  - `socket`
  - `os`
  - `mimetypes`

## Структура проекта
- `server.py` — код HTTP-сервера
- `index.html` — HTML-страница, отдаваемая сервером
  
## Как работает сервер
1. Создаётся TCP-сокет и привязывается к адресу `localhost:9093`.
2. Сервер ждёт подключения клиентов.
3. При получении HTTP-запроса сервер:
   - разбирает метод и путь;
   - обрабатывает только метод **GET**;
   - по умолчанию отдаёт `index.html`;
   - определяет MIME-тип файла;
   - формирует корректный HTTP-ответ и отправляет клиенту.
4. При ошибках возвращаются страницы с кодами:
   - **404 Not Found** — файл не найден;
   - **405 Method Not Allowed** — если запрос не GET;
   - **500 Internal Server Error** — при сбое обработки.

## Запуск сервера
### Шаг 1: Запуск HTTP-сервера
Откройте терминал и выполните:
```bash
cd Task3
python3 server.py
```
Сервер запустится на localhost:8082 и будет ожидать HTTP-запросы.

### Шаг 2: Открытие в браузере
Откройте браузер и перейдите по адресу:
```
http://localhost:8082
```

Вы увидите красивую HTML-страницу с информацией о выполненном задании.

**Остановка**

Для завершения работы сервера нажмите Ctrl+C в терминале.

## Обработка ошибок

### 404 Not Found
Если запрашиваемый файл не найден, сервер возвращает страницу с ошибкой 404.

### 500 Internal Server Error
При внутренних ошибках сервера возвращается страница с ошибкой 500.

### 405 Method Not Allowed
Сервер поддерживает только GET-запросы.

## Код:

**server.py**
```python
import socket
import mimetypes

HOST = 'localhost'
PORT = 9093


def get_file_content(filename):
    try:
        with open(filename, 'rb') as file:
            return file.read()
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Ошибка чтения файла {filename}: {e}")
        return None


def get_content_type(filename):
    """Определение MIME-типа файла"""
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type if mime_type else 'text/plain'

def create_http_response(status_code, content_type, content):
    """Создание HTTP-ответа"""
    status_messages = {
        200: "OK",
        404: "Not Found",
        500: "Internal Server Error"
    }

    status_line = f"HTTP/1.1 {status_code} {status_messages.get(status_code, 'Unknown')}"
    headers = [
        f"Content-Type: {content_type}; charset=UTF-8",
        f"Content-Length: {len(content)}",
        "Connection: close",
        "Server: Python-HTTP-Server/1.0"
    ]

    response = f"{status_line}\r\n"
    response += "\r\n".join(headers)
    response += "\r\n\r\n"

    return response.encode('utf-8') + content


def handle_request(request_data):
    """Обработка HTTP-запроса"""
    try:
        lines = request_data.decode('utf-8').split('\n')
        if not lines:
            return create_http_response(400, 'text/plain', b'Bad Request')

        request_line = lines[0].strip()
        parts = request_line.split()

        if len(parts) < 2:
            return create_http_response(400, 'text/plain', b'Bad Request')

        method = parts[0]
        path = parts[1]

        print(f"Запрос: {method} {path}")

        # Обрабатываем только GET запросы
        if method != 'GET':
            return create_http_response(405, 'text/plain', b'Method Not Allowed')

        # По умолчанию отдаем index.html
        if path == '/' or path == '/index.html':
            filename = 'index.html'
        else:
            filename = path.lstrip('/')

        # Читаем содержимое файла
        content = get_file_content(filename)

        if content is None:
            # Файл не найден
            error_content = """
            <html>
            <head><title>404 Not Found</title></head>
            <body>
                <h1>404 - Страница не найдена</h1>
                <p>Запрашиваемый файл не найден на сервере.</p>
                <a href="/">Вернуться на главную</a>
            </body>
            </html>
            """.encode('utf-8')
            return create_http_response(404, 'text/html', error_content)

        # Определяем MIME-тип
        content_type = get_content_type(filename)

        # Создаем успешный ответ
        return create_http_response(200, content_type, content)

    except Exception as e:
        print(f"Ошибка обработки запроса: {e}")
        error_content = """
        <html>
        <head><title>500 Internal Server Error</title></head>
        <body>
            <h1>500 - Внутренняя ошибка сервера</h1>
            <p>Произошла ошибка при обработке запроса.</p>
        </body>
        </html>
        """.encode('utf-8')
        return create_http_response(500, 'text/html', error_content)


def main():
    """Основная функция сервера"""
    # Создаем TCP сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Позволяем повторно использовать адрес
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        # Привязываем сокет к адресу и порту
        server_socket.bind((HOST, PORT))

        # Начинаем слушать входящие соединения
        server_socket.listen(5)
        print(f"HTTP сервер запущен на {HOST}:{PORT}")
        print("Откройте браузер и перейдите по адресу: http://localhost:9093")
        print("Для остановки сервера нажмите Ctrl+C")

        while True:
            # Принимаем соединение от клиента
            client_connection, client_address = server_socket.accept()
            print(f'Подключение от {client_address}')

            try:
                # Получаем HTTP-запрос
                request_data = client_connection.recv(4096)

                if request_data:
                    # Обрабатываем запрос и получаем ответ
                    response = handle_request(request_data)

                    # Отправляем ответ клиенту
                    client_connection.sendall(response)
                    print(f'Ответ отправлен клиенту {client_address}')

            except Exception as e:
                print(f"Ошибка при обработке клиента {client_address}: {e}")
            finally:
                # Закрываем соединение
                client_connection.close()

    except KeyboardInterrupt:
        print("\nСервер остановлен пользователем")
    except Exception as e:
        print(f"Ошибка сервера: {e}")
    finally:
        # Закрываем сокет
        server_socket.close()
        print("Сервер завершил работу")


if __name__ == "__main__":
    main()

```
**index.html**
```html
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <title>Web-программирование — ЛР1, Задание 3</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 2rem;
      background: #121212;
      color: #f0f0f0;
      text-align: center;
      line-height: 1.6;
    }
    h1 {
      font-size: 1.6rem;
      margin-bottom: 1rem;
    }
    p {
      margin: 0.5rem 0;
    }
    footer {
      margin-top: 3rem;
    }
    footer img {
      display: block;
      margin: 0 auto;
      max-width: 200px;
      height: auto;
    }
  </style>
</head>
<body>
  <h1>Web-программирование</h1>
  <p>Лабораторная работа 1</p>
  <p>Задание 3</p>
  <p><strong>Мой Python-сервер передаёт привет!</strong></p>
  <p>Эта страница была загружена с помощью сокетов.</p>

<footer>
    <img src="/img/2.png" alt="Котик пишет код">
    <p class="greeting">Хорошего дня!</p>
  </footer>
</body>
</html>
```
---
# Задание 4

---

## Описание
Реализованы клиентская и серверная части **многопользовательского чата** на Python с использованием библиотеки **socket** и протокола **TCP**.  
Для одновременной работы нескольких клиентов используется **threading**.

- Каждый клиент при подключении отправляет серверу свой **никнейм**.
- Все сообщения клиента рассылаются **всем остальным** участникам.
- Команда выхода: **`/quit`**.

## Требования
- Python 3.6+
- Стандартные библиотеки:
  - `socket`
  - `threading`

## Структура проекта
- `server.py` — TCP-сервер: принимает подключения, хранит список клиентов, рассылает сообщения.
- `client.py` — TCP-клиент: отправляет сообщения и получает рассылку в отдельном потоке.

## Как работает программа
1. Сервер создаёт TCP-сокет и слушает `127.0.0.1:9094`.
2. Клиент подключается к серверу, **вводит ник** и отправляет его первой строкой.
3. Сервер сохраняет сокет клиента и ник; оповещает остальных о подключении.
4. Любое сообщение клиента пересылается сервером всем остальным участникам.
5. При вводе `/quit` клиент отключается; сервер уведомляет остальных.


## Запуск

### Шаг 1: Запуск сервера
Откройте терминал и выполните:
```bash
cd Task4
python3 server.py
```
### Шаг 2: Запуск клиента
В другом терминале выполните:
```bash
python3 client.py
```
### Шаг 3: Начните переписку
Пример:
```
Введите ник: Ананас
> Привет
```

### Пример работы
Клиент A
```
Введите ник: Ананас
>
[+] Ананас присоединился
>
[+] Яблоко присоединился
>
[+] Груша присоединился
> Привет
>
Яблоко: Пока
>
Груша: окак
>
```
Клиент B
```
Введите ник: Яблоко

[+] Яблоко присоединился
> >
[+] Груша присоединился
>
Ананас: Привет
> Пока
>
Груша: окак
>
```

Клиент C
```
Введите ник: Груша
>
[+] Груша присоединился
>
Ананас: Привет
>
Яблоко: Пока
> окак
>
```

Сервер
```
('127.0.0.1', 63575) -> Ананас
('127.0.0.1', 63629) -> Яблоко
('127.0.0.1', 63708) -> Груша
```

## Код:

**server.py**
```python
import socket
import threading

HOST = "127.0.0.1"
PORT = 9094

clients = []
nicknames = {}
lock = threading.Lock()


def broadcast(text, sender=None):
    """Отправка текстового сообщения всем клиентам."""
    dead = []
    with lock:
        for sock in clients:
            if sender is not None and sock is sender:
                continue
            try:
                sock.sendall((text + "\n").encode("utf-8"))
            except OSError:
                dead.append(sock)
        for s in dead:
            if s in clients:
                clients.remove(s)
            nicknames.pop(s, None)
            try:
                s.close()
            except OSError:
                pass


def handle_client(sock, addr):
    """Обработка одного клиента в отдельном потоке."""
    try:
        # первая полученная строка — ник
        raw = sock.recv(1024)
        nickname = raw.decode("utf-8").strip() if raw else ""
        if not nickname:
            nickname = f"user_{addr[1]}"

        with lock:
            clients.append(sock)
            nicknames[sock] = nickname

        broadcast(f"[+] {nickname} присоединился")
        print(f"{addr} -> {nickname}")

        while True:
            data = sock.recv(4096)
            if not data:
                break
            msg = data.decode("utf-8").rstrip("\r\n")
            if msg.lower() == "/quit":
                break
            broadcast(f"{nickname}: {msg}", sender=sock)
    except OSError:
        pass
    finally:
        with lock:
            if sock in clients:
                clients.remove(sock)
            name = nicknames.pop(sock, "unknown")
        broadcast(f"[-] {name} вышел")
        try:
            sock.close()
        except OSError:
            pass
        print(f"{addr} disconnected")


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(10)
    print(f"Сервер: {HOST}:{PORT}")

    try:
        while True:
            client_sock, client_addr = server.accept()
            threading.Thread(
                target=handle_client, args=(client_sock, client_addr), daemon=True
            ).start()
    except KeyboardInterrupt:
        print("\nСтоп")
    finally:
        with lock:
            for s in clients:
                try:
                    s.close()
                except OSError:
                    pass
            clients.clear()
            nicknames.clear()
        server.close()


if __name__ == "__main__":
    main()
```

**client.py**
```python
import socket
import threading

HOST = "127.0.0.1"
PORT = 9094

print_lock = threading.Lock()


def receiver(sock: socket.socket) -> None:
    """Читает входящие сообщения и печатает их с новой строки."""
    try:
        while True:
            data = sock.recv(4096)
            if not data:
                with print_lock:
                    print("\n[Соединение закрыто сервером]")
                break
            text = data.decode("utf-8")
            with print_lock:
                # печатаем входящее и возвращаем
                print(f"\n{text}", end="")
                print("> ", end="", flush=True)
    except OSError:
        pass
    finally:
        try:
            sock.close()
        except OSError:
            pass


def main() -> None:
    nickname = input("Введите ник: ").strip() or "user"

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    # отправляем ник первой строкой
    sock.sendall((nickname + "\n").encode("utf-8"))

    # запускаем поток-приёмник
    threading.Thread(target=receiver, args=(sock,), daemon=True).start()
    
    #Чтобы было можно печать во время отправки сообщений
    with print_lock:
        print("> ", end="", flush=True)

    try:
        while True:
            msg = input()
            if msg.strip().lower() == "/quit":
                sock.sendall(b"/quit\n")
                break
            sock.sendall((msg + "\n").encode("utf-8"))
            with print_lock:
                print("> ", end="", flush=True)
    except KeyboardInterrupt:
        pass
    finally:
        try:
            sock.close()
        except OSError:
            pass
        with print_lock:
            print("\nКлиент завершил работу")


if __name__ == "__main__":
    main()

```
---

# Задание 5

---

## Описание

Реализована серверная часть приложения на Python c использованием `socket`.
Клиент открывает страницу журнала `index.html`.
Сервер принимает оценки через **POST**, сохраняет их в `grades.json` и на **GET** отдаёт HTML-страницу со сводной таблицей (одна строка на дисциплину, в ячейке — список её оценок).

## Требования

* Python 3.7+
* Стандартные библиотеки:

  * `socket`
  * `urllib.parse`
  * `json`
  * `os`

## Структура проекта

* `server.py` — HTTP-сервер (обрабатывает `GET /` и `POST /add`)
* `data_store.py` — простое хранилище данных (чтение/запись `grades.json`)
* `index.html` — HTML-шаблон страницы журнала
* `grades.json` — файл с данными (создаётся автоматически при первой записи)

## Коды ответов:

   * **200 OK** — успешная выдача страницы,
   * **303 See Other** — после успешного `POST`,
   * **400 Bad Request** — некорректный формат запроса,
   * **404 Not Found** — неизвестный путь,
   * **405 Method Not Allowed** — методы, кроме GET/POST.

## Клиентская валидация

В `index.html` есть JavaScript-проверка: при неверной оценке кнопка «Добавить» загорается красным, показана подсказка, отправка формы блокируется.
Серверная проверка остаётся обязательной (на случай обхода фронтенда).

## Запуск сервера

### Шаг 1: запуск

Откройте терминал в папке проекта и выполните:

```bash
python server.py
```

### Шаг 2: открыть в браузере

Перейдите по адресу:

```
http://127.0.0.1:8080
```

Вы увидите страницу «Журнал оценок» с формой добавления и таблицей.

**Остановка:** `Ctrl + C` в терминале.


## Формат данных

Файл `grades.json` хранит словарь «дисциплина → список оценок», например:

```json
{
  "Математика": ["5", "4"],
  "Физика": ["0,01"]
}
```

## Код:

**data_store.py**
```python
"""
Формат файла grades.json:
{
  "Математика": ["5", "4"],
  "Физика": ["0,01"]
}
"""

import json
import os
from typing import Dict, List

FILE_PATH = "grades.json"


def _load() -> Dict[str, List[str]]:
    """Загружаем словарь дисциплин и оценок из JSON, если файла нет — пустой словарь."""
    if not os.path.exists(FILE_PATH):
        return {}
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def _save(data: Dict[str, List[str]]) -> None:
    """Сохраняем словарь в JSON."""
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_grade(discipline: str, grade: str) -> None:
    """Добавляем оценку к дисциплине."""
    data = _load()
    discipline = discipline.strip()
    grade = grade.strip()
    if not discipline or not grade:
        return
    data.setdefault(discipline, []).append(grade)
    _save(data)


def get_all() -> Dict[str, List[str]]:
    """Возвращаем весь журнал."""
    return _load()

```
## Код:

**server.py**
```python
import socket
import urllib.parse
from typing import Tuple, Dict
import data_store

HOST = "127.0.0.1"
PORT = 9095


def build_response(status: str, headers: Dict[str, str], body: str = "") -> bytes:
    """Формируем HTTP-ответ."""
    body_bytes = body.encode("utf-8")
    headers = {
        "Content-Type": "text/html; charset=utf-8",
        "Connection": "close",
        "Content-Length": str(len(body_bytes)),
        **headers,
    }
    lines = [f"HTTP/1.1 {status}"] + [f"{k}: {v}" for k, v in headers.items()]
    head = "\r\n".join(lines) + "\r\n\r\n"
    return head.encode("utf-8") + body_bytes


def parse_request(data: bytes) -> Tuple[str, str, Dict[str, str], bytes]:
    try:
        head, body = data.split(b"\r\n\r\n", 1)
    except ValueError:
        return "", "", {}, b""

    lines = head.decode("iso-8859-1").split("\r\n")
    if not lines or " " not in lines[0]:
        return "", "", {}, b""

    method, path, *_ = lines[0].split(" ")

    headers: Dict[str, str] = {}
    for line in lines[1:]:
        if ":" in line:
            k, v = line.split(":", 1)
            headers[k.strip().lower()] = v.strip()

    return method, path, headers, body


def handle_get(path: str) -> bytes:
    """Обработка GET-запросов."""
    if path == "/":
        data = data_store.get_all()
        disciplines = sorted(data.keys(), key=lambda s: s.lower())

        # Формируем строки таблицы
        rows = []
        for d in disciplines:
            grades = "; ".join(escape_html(g) for g in data[d])
            rows.append(f"<tr><td>{escape_html(d)}</td><td>{grades}</td></tr>")
        rows_html = "\n".join(rows) if rows else '<tr><td colspan="2">Пока пусто</td></tr>'

        # Читаем index.html
        try:
            with open("index.html", "r", encoding="utf-8") as f:
                template = f.read()
        except FileNotFoundError:
            return build_response("500 Internal Server Error", {}, "index.html not found")

        html = template.replace("{{rows}}", rows_html)
        return build_response("200 OK", {}, html)

    return build_response("404 Not Found", {}, "Not Found")


def _is_positive_number(text: str) -> bool:
    """
    Возвращает True, если строка — положительное число > 0.
    """
    norm = text.replace(",", ".")
    try:
        return float(norm) > 0.0
    except ValueError:
        return False


def handle_post(path: str, headers: Dict[str, str], body: bytes) -> bytes:
    """Обработка POST-запросов."""
    if path == "/add":
        if "application/x-www-form-urlencoded" not in headers.get("content-type", ""):
            return build_response("400 Bad Request", {}, "Expected x-www-form-urlencoded")

        form = urllib.parse.parse_qs(body.decode("utf-8"), keep_blank_values=True)
        discipline = (form.get("discipline", [""])[0]).strip()
        grade_raw = (form.get("grade", [""])[0]).strip()

        # Серверная проверка: положительное число > 0 (целое или дробное, . или ,)
        if discipline and _is_positive_number(grade_raw):
            data_store.add_grade(discipline, grade_raw)

        return build_response("303 See Other", {"Location": "/"}, "")

    return build_response("404 Not Found", {}, "Not Found")


def escape_html(s: str) -> str:
    """Экранирование спецсимволов в HTML."""
    return (
        s.replace("&", "&amp;")
         .replace("<", "&lt;")
         .replace(">", "&gt;")
         .replace('"', "&quot;")
         .replace("'", "&#39;")
    )


def serve():
    """Главный цикл сервера."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORT))
        srv.listen(5)
        print(f"Server running at http://{HOST}:{PORT}")

        while True:
            conn, _ = srv.accept()
            with conn:
                try:
                    raw = conn.recv(65535)
                    method, path, headers, body = parse_request(raw)
                    length = int(headers.get("content-length", "0"))
                    while len(body) < length:
                        chunk = conn.recv(65535)
                        if not chunk:
                            break
                        body += chunk
                except (socket.timeout, ValueError, UnicodeDecodeError):
                    conn.sendall(build_response("400 Bad Request", {}, "Bad Request"))
                    continue

                if method == "GET":
                    resp = handle_get(path)
                elif method == "POST":
                    resp = handle_post(path, headers, body)
                else:
                    resp = build_response("405 Method Not Allowed", {"Allow": "GET, POST"}, "Method Not Allowed")

                conn.sendall(resp)


if __name__ == "__main__":
    serve()

```

## Код:

**index.html**
```html
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8"/>
  <title>Журнал</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #f0f0f0;
      margin: 0;
      padding: 0;
    }
    .container {
      max-width: 800px;
      margin: 40px auto;
      background: #fff;
      padding: 24px;
      border-radius: 8px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    h1 {
      margin-top: 0;
      color: #333;
    }
    form {
      margin: 20px 0;
      display: grid;
      grid-template-columns: 1fr 1fr auto;
      gap: 10px;
      align-items: center;
    }
    input, button {
      padding: 10px;
      font-size: 14px;
    }
    input {
      border: 1px solid #ccc;
      border-radius: 4px;
    }
    .btn {
      background-color: #4a4a4a;
      color: #fff;
      border: none;
      cursor: pointer;
      border-radius: 4px;
      transition: background 0.2s, transform 0.05s;
    }
    .btn:hover { background-color: #333; }
    .btn:active { transform: translateY(1px); }
    /* Состояние ошибки: красная кнопка */
    .btn.error { background-color: #c62828; }
    .hint {
      grid-column: 1 / -1;
      color: #a00;
      font-size: 13px;
      display: none;
      margin-top: -6px;
    }
    .hint.show { display: block; }

    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 16px;
    }
    th, td {
      border: 1px solid #ccc;
      padding: 10px;
      text-align: left;
    }
    th { background: #eee; }
    tr:nth-child(even) { background: #fafafa; }
  </style>
</head>
<body>
  <div class="container">
    <h1>Журнал</h1>

    <form id="grade-form" method="POST" action="/add" novalidate>
      <input id="discipline" name="discipline" placeholder="Дисциплина" required />
      <input id="grade" name="grade" placeholder="Оценка (> 0, можно дробную)" required />
      <button id="submitBtn" class="btn" type="submit">Добавить</button>
      <div id="hint" class="hint">
        Оценка должна быть положительным числом (целым или дробным; разделитель «.» или «,»).
      </div>
    </form>

    <table>
      <tr><th>Дисциплина</th><th>Оценки</th></tr>
      {{rows}}
    </table>
  </div>

  <script>
    // Клиентская валидация: положительное число > 0, допускаем дробные с . или ,
    (function () {
      const form = document.getElementById('grade-form');
      const gradeInput = document.getElementById('grade');
      const submitBtn = document.getElementById('submitBtn');
      const hint = document.getElementById('hint');

      function isPositiveNumber(value) {
        // Разрешаем форму: "123", "0,5", "4.25"
        const trimmed = value.trim();
        if (!/^\d+([.,]\d+)?$/.test(trimmed)) return false;
        const num = parseFloat(trimmed.replace(',', '.'));
        return Number.isFinite(num) && num > 0;
      }

      function clearError() {
        submitBtn.classList.remove('error');
        hint.classList.remove('show');
      }

      gradeInput.addEventListener('input', clearError);
      form.addEventListener('input', clearError);

      form.addEventListener('submit', function (e) {
        const grade = gradeInput.value;
        if (!isPositiveNumber(grade)) {
          e.preventDefault();
          submitBtn.classList.add('error');
          hint.classList.add('show');
        }
      });
    })();
  </script>
</body>
</html>

```

