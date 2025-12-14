# Лабораторная работа 1. Работа с сокетами

## Задание 1: UDP клиент-сервер

Реализован простой обмен сообщениями по протоколу UDP.

### Сервер (task1_server.py)

Сервер создает UDP сокет, привязывается к порту 8888 и ожидает сообщения от клиентов. При получении сообщения выводит его на экран и отправляет ответ "Hello, client".

```1:15:students/k3340/Gelm_Daniil/lab1/1/task1_server.py
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('localhost', 8888))

print("Сервер запущен на порту 8888")

while True:
    data, addr = server_socket.recvfrom(1024)
    message = data.decode('utf-8')
    print(f"Получено сообщение от {addr}: {message}")
    
    response = "Hello, client"
    server_socket.sendto(response.encode('utf-8'), addr)
    print(f"Отправлен ответ: {response}")
```

### Клиент (task1_client.py)

Клиент отправляет сообщение "Hello, server" на сервер и выводит полученный ответ.

```1:15:students/k3340/Gelm_Daniil/lab1/1/task1_client.py
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 8888)
message = "Hello, server"

client_socket.sendto(message.encode('utf-8'), server_address)
print(f"Отправлено сообщение: {message}")

data, addr = client_socket.recvfrom(1024)
response = data.decode('utf-8')
print(f"Получен ответ от сервера: {response}")

client_socket.close()
```

## Задание 2: TCP клиент-сервер для теоремы Пифагора

Реализован TCP сервер, который вычисляет гипотенузу по двум катетам, используя теорему Пифагора.

### Сервер (task2_server.py)

Сервер принимает TCP подключения, получает два числа через запятую, вычисляет гипотенузу и отправляет результат обратно клиенту.

```1:26:students/k3340/Gelm_Daniil/lab1/2/task2_server.py
import socket
import math

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8889))
server_socket.listen(5)

print("Сервер запущен на порту 8889")

def pythagorean(a, b):
    return math.sqrt(a * a + b * b)

while True:
    client_socket, addr = server_socket.accept()
    print(f"Подключен клиент: {addr}")
    
    data = client_socket.recv(1024).decode('utf-8')
    try:
        a, b = map(float, data.split(','))
        result = pythagorean(a, b)
        response = str(result)
    except:
        response = "Ошибка: некорректные данные"
    
    client_socket.send(response.encode('utf-8'))
    client_socket.close()
```

### Клиент (task2_client.py)

Клиент запрашивает у пользователя два катета, отправляет их на сервер и выводит полученный результат.

```1:17:students/k3340/Gelm_Daniil/lab1/2/task2_client.py
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8889))

print("Введите два катета для теоремы Пифагора:")
a = float(input("Катет a: "))
b = float(input("Катет b: "))

data = f"{a},{b}"
client_socket.send(data.encode('utf-8'))

result = client_socket.recv(1024).decode('utf-8')
print(f"Гипотенуза: {result}")

client_socket.close()
```

## Задание 3: HTTP сервер

Реализован HTTP сервер, который отдает HTML страницу из файла index.html.

### Сервер (task3_server.py)

Сервер загружает содержимое файла index.html при старте и отдает его в ответ на любой HTTP запрос с правильными заголовками.

```1:32:students/k3340/Gelm_Daniil/lab1/3/task3_server.py
import socket

def load_html(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return "<html><body><h1>Ошибка загрузки файла</h1></body></html>"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8890))
server_socket.listen(5)

print("HTTP сервер запущен на порту 8890")

html_content = load_html('index.html')

while True:
    client_socket, addr = server_socket.accept()
    print(f"Подключен клиент: {addr}")
    
    request = client_socket.recv(1024).decode('utf-8')
    
    response = f"HTTP/1.1 200 OK\r\n"
    response += f"Content-Type: text/html; charset=utf-8\r\n"
    response += f"Content-Length: {len(html_content.encode('utf-8'))}\r\n"
    response += f"\r\n"
    response += html_content
    
    client_socket.send(response.encode('utf-8'))
    client_socket.close()
```

### HTML файл (index.html)

Простая HTML страница для тестирования сервера.

## Задание 4: Многопользовательский чат

Реализован многопользовательский чат на TCP с использованием потоков для обработки нескольких клиентов одновременно.

### Сервер (task4_server.py)

Сервер поддерживает несколько подключений через threading. Каждый клиент обрабатывается в отдельном потоке. Сообщения от одного клиента рассылаются всем остальным подключенным клиентам.

```1:46:students/k3340/Gelm_Daniil/lab1/4/task4_server.py
import socket
import threading

clients = []
lock = threading.Lock()

def handle_client(client_socket, addr):
    print(f"Подключен клиент: {addr}")
    with lock:
        clients.append(client_socket)
    
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            
            message = data.decode('utf-8')
            print(f"Сообщение от {addr}: {message}")
            
            with lock:
                for client in clients:
                    if client != client_socket:
                        try:
                            client.send(f"{addr}: {message}".encode('utf-8'))
                        except:
                            pass
        except:
            break
    
    with lock:
        clients.remove(client_socket)
    client_socket.close()
    print(f"Клиент {addr} отключен")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8891))
server_socket.listen(10)

print("Чат сервер запущен на порту 8891")

while True:
    client_socket, addr = server_socket.accept()
    thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    thread.start()
```

### Клиент (task4_client.py)

Клиент использует отдельный поток для приема сообщений от сервера, основной поток используется для ввода и отправки сообщений.

```1:30:students/k3340/Gelm_Daniil/lab1/4/task4_client.py
import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            print(data.decode('utf-8'))
        except:
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8891))

recv_thread = threading.Thread(target=receive_messages, args=(client_socket,))
recv_thread.daemon = True
recv_thread.start()

print("Подключен к чату. Введите сообщение:")

while True:
    message = input()
    if message == '/quit':
        break
    client_socket.send(message.encode('utf-8'))

client_socket.close()
```

## Задание 5: Веб-сервер для журнала оценок

Реализован веб-сервер для обработки GET и POST запросов. Сервер позволяет добавлять оценки по дисциплинам через POST запрос и просматривать журнал через GET запрос.

### Сервер (task5_server.py)

Сервер хранит оценки в словаре, где ключ - название дисциплины, значение - список оценок. При POST запросе парсит данные формы и добавляет оценку в соответствующий список. При любом запросе генерирует и отдает HTML страницу с формой добавления и таблицей всех оценок.

```1:84:students/k3340/Gelm_Daniil/lab1/5/task5_server.py
import socket
import urllib.parse

grades = {}

def generate_html():
    html = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Журнал оценок</title>
    <style>
        body { font-family: Arial; margin: 20px; }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        form { margin-bottom: 20px; }
        input, button { padding: 5px; margin: 5px; }
    </style>
</head>
<body>
    <h1>Журнал оценок</h1>
    <form method="POST" action="/">
        <input type="text" name="discipline" placeholder="Дисциплина" required>
        <input type="number" name="grade" placeholder="Оценка" min="1" max="5" required>
        <button type="submit">Добавить оценку</button>
    </form>
    <table>
        <tr>
            <th>Дисциплина</th>
            <th>Оценки</th>
        </tr>"""
    
    for discipline, grade_list in grades.items():
        grades_str = ', '.join(map(str, grade_list))
        html += f"<tr><td>{discipline}</td><td>{grades_str}</td></tr>"
    
    html += """</table>
</body>
</html>"""
    return html

def parse_post(data):
    params = {}
    if '\r\n\r\n' in data:
        parts = data.split('\r\n\r\n', 1)
        if len(parts) > 1:
            body = parts[1]
            for pair in body.split('&'):
                if '=' in pair:
                    key, value = pair.split('=', 1)
                    params[urllib.parse.unquote(key)] = urllib.parse.unquote(value)
    return params

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8892))
server_socket.listen(5)

print("Веб-сервер запущен на порту 8892")

while True:
    client_socket, addr = server_socket.accept()
    request = client_socket.recv(4096).decode('utf-8')
    
    if request.startswith('POST'):
        params = parse_post(request)
        discipline = params.get('discipline', '')
        grade = params.get('grade', '')
        
        if discipline and grade:
            if discipline not in grades:
                grades[discipline] = []
            grades[discipline].append(int(grade))
    
    html_content = generate_html()
    
    response = "HTTP/1.1 200 OK\r\n"
    response += "Content-Type: text/html; charset=utf-8\r\n"
    response += f"Content-Length: {len(html_content.encode('utf-8'))}\r\n"
    response += "\r\n"
    response += html_content
    
    client_socket.send(response.encode('utf-8'))
    client_socket.close()
```

### Основные особенности реализации

- Оценки хранятся структурированно: каждая дисциплина имеет список всех оценок
- POST запросы парсятся вручную с декодированием URL-encoded данных
- HTML генерируется динамически на основе текущего состояния словаря grades
- Оценки отображаются в таблице, где каждая строка содержит дисциплину и все ее оценки через запятую

