# Отчет по лабораторной работе 1

## Задание 1: UDP клиент-сервер (Hello, server/client)

**Описание:**  
Реализована клиентская и серверная часть приложения на протоколе UDP. Клиент отправляет серверу сообщение `"Hello, server"`, сервер принимает сообщение и отвечает `"Hello, client"`.

**Код сервера (`udp_server.py`):**
```python
import socket

# Создаем UDP-сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Привязываем сокет к адресу и порту
server_socket.bind(('localhost', 8080))
print("UDP сервер запущен на порту 8080...")

while True:
    # Принимаем сообщение от клиента
    data, client_address = server_socket.recvfrom(1024)
    print(f"Получено от {client_address}: {data.decode()}")

    # Отправляем ответ
    response = "Hello, client"
    server_socket.sendto(response.encode(), client_address)
```

**Код клиента (`udp_client.py`):**

```python
import socket

# Создаем UDP-сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Отправляем сообщение серверу
message = "Hello, server"
client_socket.sendto(message.encode(), ('localhost', 8080))

# Получаем ответ от сервера
data, server_address = client_socket.recvfrom(1024)
print(f"Ответ от сервера: {data.decode()}")

# Закрываем сокет
client_socket.close()

```

---

## Задание 2: TCP клиент-сервер (вычисление площади параллелограмма)

**Описание:**
Клиент вводит параметры параллелограмма, сервер вычисляет площадь и возвращает результат. Протокол TCP.

**Код сервера (`tcp_server.py`):**

```python
import socket

# Создаем UDP-сокет для приема и отправки сообщений
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Привязываем сокет к локальному адресу и порту 8080
server_socket.bind(('localhost', 8080))
print("UDP сервер запущен на порту 8080...")

while True:
    # Ждем данные от клиента
    data, client_address = server_socket.recvfrom(1024)
    message = data.decode()
    print(f"Запрос от клиента {client_address}: {message}")

    try:
        # Преобразуем строку в два числа и вычисляем площадь
        a, h = map(float, message.split())
        area = a * h
        response = f"Площадь параллелограмма = {area}"
    except Exception as e:
        # Если данные некорректные, формируем сообщение об ошибке
        response = f"Ошибка: {e}"

    # Отправляем результат обратно клиенту
    server_socket.sendto(response.encode(), client_address)

```

**Код клиента (`tcp_client.py`):**

```python
import socket

# Создаем UDP-сокет для отправки и получения данных
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Вводим данные параллелограмма от пользователя
a = input("Введите основание параллелограмма: ")
h = input("Введите высоту параллелограмма: ")

# Формируем сообщение в виде строки и отправляем серверу
message = f"{a} {h}"
client_socket.sendto(message.encode(), ('localhost', 8080))

# Получаем ответ от сервера и выводим его
data, server_address = client_socket.recvfrom(1024)
print(f"Ответ от сервера: {data.decode()}")

# Закрываем соединение, освобождая ресурсы
client_socket.close()

```

---

## Задание 3: HTTP сервер (отдача HTML-страницы)

**Описание:**
Сервер принимает TCP-подключение, возвращает HTML-страницу из файла `index.html` в виде HTTP-ответа.

**Код сервера (`http_server.py`):**

```python
import socket

# Настройки сервера
HOST = 'localhost'  # Сервер будет работать на локальной машине
PORT = 8080         # Порт для подключения клиентов

# Создаем TCP-сокет (для HTTP нужен TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет к адресу и порту
server_socket.bind((HOST, PORT))

# Начинаем слушать входящие соединения, максимум 1 в очереди
server_socket.listen(1)

print(f"HTTP сервер запущен на http://{HOST}:{PORT}")

while True:
    # Ожидаем подключение клиента
    client_connection, client_address = server_socket.accept()
    print(f"Подключение от {client_address}")

    # Получаем HTTP-запрос от клиента
    request = client_connection.recv(1024).decode()
    print("Запрос клиента:")
    print(request)

    # Читаем содержимое HTML-файла для ответа
    with open("/Users/glavnipopivy/UCHEBA/web-prog/TonikX-ITMO_ICT_WebDevelopment_2025-2026/lab1/Task 3/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    # Формируем HTTP-ответ
    response = (
        "HTTP/1.1 200 OK\r\n"                         # Статус ответа
        "Content-Type: text/html; charset=utf-8\r\n"  # Тип контента
        f"Content-Length: {len(html_content.encode())}\r\n"  # Длина содержимого
        "\r\n"                                        # Пустая строка отделяет заголовки от тела
        f"{html_content}"                             # Тело ответа (HTML)
    )

    # Отправляем ответ клиенту
    client_connection.sendall(response.encode())

    # Закрываем соединение с клиентом
    client_connection.close()

```

---

## Задание 4: Многопользовательский чат (TCP + threading)

**Описание:**
Реализован многопользовательский чат с использованием потоков (`threading`). Сервер обрабатывает сообщения всех клиентов, рассылая их остальным пользователям.

**Код сервера (`chat_server.py`):**

```python
import socket

# Создаем UDP-сокет для приема и отправки сообщений
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Привязываем сокет к локальному адресу и порту 8080
server_socket.bind(('localhost', 8080))
print("UDP сервер запущен на порту 8080...")

while True:
    # Ждем данные от клиента
    data, client_address = server_socket.recvfrom(1024)
    message = data.decode()
    print(f"Запрос от клиента {client_address}: {message}")

    try:
        # Преобразуем строку в два числа и вычисляем площадь
        a, h = map(float, message.split())
        area = a * h
        response = f"Площадь параллелограмма = {area}"
    except Exception as e:
        # Если данные некорректные, формируем сообщение об ошибке
        response = f"Ошибка: {e}"

    # Отправляем результат обратно клиенту
    server_socket.sendto(response.encode(), client_address)
```

**Код клиента (`chat_client.py`):**

```python
import socket
import threading

HOST = "localhost"  # Адрес сервера
PORT = 8080         # Порт сервера

# Функция для получения сообщений от сервера в отдельном потоке
def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)  # Получаем данные от сервера
            if not data:             # Если сервер закрыл соединение
                break
            print(data.decode("utf-8"))  # Выводим полученное сообщение
        except:
            break

# Создаем TCP-сокет и подключаемся к серверу
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

# Запускаем отдельный поток для получения сообщений от сервера
threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

try:
    while True:
        # Вводим сообщение и отправляем на сервер
        msg = input()
        sock.sendall(msg.encode("utf-8"))
except KeyboardInterrupt:
    # Завершаем работу при Ctrl+C
    print("\nВыход...")
finally:
    # Закрываем соединение
    sock.close()
```

---

## Задание 5: Веб-сервер с обработкой GET/POST

**Описание:**
Сервер принимает данные дисциплины и оценки через POST-запрос, хранит их в словаре и отображает все оценки в HTML-таблице.

**Код сервера (`get_post_server.py`):**

```python
import socket
from urllib.parse import unquote_plus  # Для декодирования данных формы из URL-кодировки

HOST = "localhost"
PORT = 8080

grades = {}  # Словарь для хранения оценок по дисциплинам

def build_html():
    """Создает HTML-страницу с формой и таблицей оценок"""
    # Генерируем строки таблицы с текущими оценками
    rows = "".join(f"<tr><td>{subject}</td><td>{grade}</td></tr>" for subject, grade in grades.items())
    html = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Оценки по дисциплинам</title>
    </head>
    <body>
        <h1>Добавить оценку</h1>
        <form method="POST" action="/">
            Дисциплина: <input type="text" name="subject" required>
            Оценка: <input type="text" name="grade" required>
            <input type="submit" value="Добавить">
        </form>
        <h2>Все оценки</h2>
        <table border="1">
            <tr><th>Дисциплина</th><th>Оценка</th></tr>
            {rows}
        </table>
    </body>
    </html>
    """
    return html

def parse_post_data(body):
    data = {}
    for pair in body.split("&"):  # Каждая пара key=value
        if "=" in pair:
            key, value = pair.split("=", 1)
            data[key] = unquote_plus(value)  # Декодируем URL-кодировку
    return data

def handle_client(conn):
    try:
        request = conn.recv(4096).decode("utf-8")  # Получаем HTTP-запрос
        if not request:
            return
        headers, _, body = request.partition("\r\n\r\n")  # Разделяем заголовки и тело
        first_line = headers.splitlines()[0]  # Берем первую строку запроса
        method, path, _ = first_line.split()

        if method == "POST":
            post_data = parse_post_data(body)  # Разбираем данные формы
            subject = post_data.get("subject", "").strip()
            grade = post_data.get("grade", "").strip()
            if subject and grade:
                grades[subject] = grade  # Сохраняем оценку

        # Формируем HTML-ответ
        html_content = build_html()
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(html_content.encode('utf-8'))}\r\n"
            "\r\n"
            f"{html_content}"
        )
        conn.sendall(response.encode("utf-8"))  # Отправляем клиенту
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        conn.close()  # Закрываем соединение

# Настройка TCP-сокета сервера
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((HOST, PORT))
server_sock.listen(5)  # Максимум 5 ожидающих подключений
print(f"Сервер оценок запущен на http://{HOST}:{PORT}")

try:
    while True:
        conn, addr = server_sock.accept()  # Ожидаем подключение клиента
        handle_client(conn)  # Обрабатываем запрос
except KeyboardInterrupt:
    print("\nСервер завершён")
finally:
    server_sock.close()

```

