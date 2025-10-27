# Отчет по практической работе: Сетевое программирование на Python
## Введение
## Цель работы: Освоить основы сетевого программирования на Python с использованием библиотеки socket, реализовав различные типы клиент-серверных приложений.

**Автор:** Корольков Артем
**Дата выполнения:** Дата выполнения: 22 сентября 2025 года

## Задание 1: UDP-клиент и сервер
### Описание задания
Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.

### Ход выполнения
Серверная часть (task_1_server.py):

    import socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 12345)
    server_socket.bind(server_address)

    print("Сервер запущен и ожидает сообщений...")

    while True:
        data, client_address = server_socket.recvfrom(1024)
        print(f"Получено сообщение от {client_address}: {data.decode('utf-8')}")
    
        response = "Hello, client"
        server_socket.sendto(response.encode('utf-8'), client_address)
        print(f"Отправлен ответ: {response}")  
Клиентская часть (task_1_client.py):

    import socket

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 12345)

    message = "Hello, server"
    client_socket.sendto(message.encode('utf-8'), server_address)
    print(f"Отправлено сообщение серверу: {message}")

    data, _ = client_socket.recvfrom(1024)
    print(f"Получен ответ от сервера: {data.decode('utf-8')}")

    client_socket.close()
  
### Вывод по заданию 1
Успешно реализовано UDP-взаимодействие между клиентом и сервером. Сервер корректно принимает сообщение от клиента и отправляет ответ. Использован протокол UDP с датаграммами, что обеспечивает простоту реализации для задач, не требующих гарантированной доставки.

## Задание 2: TCP-клиент и сервер для вычисления площади трапеции
### Описание задания
Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции (поиск площади трапеции), параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

### Ход выполнения
Серверная часть (task_2_server.py):

    import socket

    def calculate_trapezoid_area(base_a, base_b, height):
        try:
            a = float(base_a)
            b = float(base_b)
            h = float(height)
            area = (a + b) * h / 2
            return f"Площадь трапеции с основаниями {a} и {b} и высотой {h} равна: {area:.2f}"
        except ValueError:
            return "Ошибка: Все параметры должны быть числами!"

    def main():
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 12346)
        server_socket.bind(server_address)
        server_socket.listen(1)
    
        print("Сервер запущен и ожидает подключений...")
    
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Подключился клиент: {client_address}")
        
            data = client_socket.recv(1024).decode('utf-8')
            print(f"Получены данные: {data}")
        
            params = data.split(',')
            if len(params) == 3:
                result = calculate_trapezoid_area(params[0], params[1], params[2])
            else:
                result = "Ошибка: Неверный формат данных."
        
            client_socket.sendall(result.encode('utf-8'))
            print(f"Отправлен результат: {result}")
            client_socket.close()
Клиентская часть (task_2_client.py):

    import socket

    def main():
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 12346)
    
        try:
            client_socket.connect(server_address)
            print("Подключение к серверу установлено")
        
            print("Введите параметры трапеции:")
            base_a = input("Основание a: ")
            base_b = input("Основание b: ")
            height = input("Высота h: ")
        
            request = f"{base_a},{base_b},{height}"
            client_socket.sendall(request.encode('utf-8'))
            print(f"Отправлен запрос: {request}")
        
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Ответ сервера: {response}")
        
        except ConnectionRefusedError:
            print("Не удалось подключиться к серверу.")
        finally:
            client_socket.close()
### Вывод по заданию 2
Реализовано TCP-взаимодействие для вычисления площади трапеции. Сервер корректно обрабатывает входящие параметры, выполняет расчет и возвращает результат. TCP-протокол обеспечивает надежную доставку данных, что важно для математических вычислений.

## Задание 3: HTTP-сервер для возврата HTML-страницы
### Описание задания
Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла index.html.

### Ход выполнения
Серверная часть (task_3_server.py):

    import socket
    import os

    def load_html_file(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            return "<html><body><h1>404 - File Not Found</h1></body></html>"

    def main():
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_address = ('localhost', 8080)
        server_socket.bind(server_address)
        server_socket.listen(5)
    
        print(f"HTTP-сервер запущен на http://{server_address[0]}:{server_address[1]}")
    
        while True:
            try:
                client_socket, client_address = server_socket.accept()
                print(f"Подключился клиент: {client_address}")
            
                request = client_socket.recv(1024).decode('utf-8')
                print(f"Получен запрос:\n{request}")
            
                html_content = load_html_file('index.html')
            
                response_headers = [
                    'HTTP/1.1 200 OK',
                    'Content-Type: text/html; charset=utf-8',
                    f'Content-Length: {len(html_content)}',
                    'Connection: close',
                    '\r\n'
                ]
            
                response = '\r\n'.join(response_headers) + html_content
                client_socket.sendall(response.encode('utf-8'))
                print("Отправлен HTTP-ответ с содержимым index.html")
            
                client_socket.close()
            
            except KeyboardInterrupt:
                break
    HTML-страница (index.html):

    html
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Тестовая страница</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            h1 { color: #333; text-align: center; }
            .container { background-color: white; padding: 20px; border-radius: 8px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Добро пожаловать на HTTP-сервер Королькова Артема!</h1>
            <p>Это тестовая страница, загружаемая сервером из файла index.html</p>
            <p>Сервер реализован на чистом Python с использованием библиотеки socket</p>
        </div>
    </body>
    </html>
### Вывод по заданию 3
Реализован простой HTTP-сервер, способный обслуживать HTML-страницы. Сервер корректно формирует HTTP-заголовки и возвращает содержимое файла index.html. Достигнута основа для понимания работы веб-серверов на низком уровне.

## Задание 4: Многопользовательский чат
### Описание задания
Реализовать многопользовательский чат с использованием потоков. Сервер должен поддерживать одновременное подключение нескольких клиентов и обеспечивать обмен сообщениями между ними.

### Ход выполнения
Серверная часть (task_4_server.py):

    import socket
    import threading

    class ChatServer:
        def __init__(self, host='localhost', port=12347):
            self.host = host
            self.port = port
            self.clients = []
            self.nicknames = []
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.lock = threading.Lock()

    def broadcast(self, message, sender_client=None):
        with self.lock:
            for client in self.clients:
                if client != sender_client:
                    try:
                        client.send(message)
                    except:
                        self.remove_client(client)

    def remove_client(self, client):
        if client in self.clients:
            index = self.clients.index(client)
            self.clients.remove(client)
            nickname = self.nicknames[index]
            self.nicknames.remove(nickname)
            self.broadcast(f'{nickname} покинул чат!'.encode('utf-8'))
            client.close()

    def handle_client(self, client):
        while True:
            try:
                message = client.recv(1024)
                if message:
                    self.broadcast(message, client)
                else:
                    self.remove_client(client)
                    break
            except:
                self.remove_client(client)
                break

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Сервер чата запущен на {self.host}:{self.port}")
        
        while True:
            client, address = self.server_socket.accept()
            print(f"Подключился клиент с адресом: {address}")
            
            client.send('NICK'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            
            with self.lock:
                self.nicknames.append(nickname)
                self.clients.append(client)
            
            print(f'Никнейм клиента: {nickname}')
            self.broadcast(f'{nickname} присоединился к чату!'.encode('utf-8'))
            client.send('Подключение к серверу успешно!'.encode('utf-8'))
            
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.daemon = True
            thread.start()
Клиентская часть (task_4_client.py):

    import socket
    import threading

    class ChatClient:
        def __init__(self, host='localhost', port=12347):
            self.host = host
            self.port = port
            self.nickname = input("Введите ваш никнейм: ")
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.client_socket.send(self.nickname.encode('utf-8'))
                else:
                    print(message)
            except:
                print("Произошла ошибка при получении сообщения!")
                self.client_socket.close()
                break

    def send_messages(self):
        while True:
            message = input()
            if message.lower() == 'quit':
                self.client_socket.close()
                break
            formatted_message = f'{self.nickname}: {message}'
            self.client_socket.send(formatted_message.encode('utf-8'))

    def start(self):
        try:
            self.client_socket.connect((self.host, self.port))
            print("Подключение к чату установлено!")
            
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            self.send_messages()
        except Exception as e:
            print(f"Ошибка подключения: {e}")
        finally:
            self.client_socket.close()
### Вывод по заданию 4
Реализован полнофункциональный многопользовательский чат с поддержкой одновременного подключения нескольких клиентов. Использование потоков позволяет эффективно обрабатывать сообщения от разных пользователей. Сервер корректно управляет подключениями и обеспечивает широковещательную рассылку сообщений.

## Задание 5: Веб-сервер для обработки GET и POST запросов
### Описание задания
Написать простой веб-сервер для обработки GET и POST HTTP-запросов. Сервер должен принимать и записывать информацию о дисциплине и оценке по дисциплине, а также отдавать информацию обо всех оценках в виде HTML-страницы.

### Ход выполнения
Серверная часть (task_5_server.py):

    import socket
    import threading
    from urllib.parse import parse_qs

    class SimpleHTTPServer:
        def __init__(self, host='localhost', port=8080):
            self.host = host
            self.port = port
            self.grades = {}
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.lock = threading.Lock()

    def handle_request(self, client_socket):
        request_data = client_socket.recv(4096).decode('utf-8')
        
        if not request_data:
            client_socket.close()
            return
        
        lines = request_data.split('\r\n')
        request_line = lines[0]
        parts = request_line.split(' ')
        
        if len(parts) < 3:
            client_socket.close()
            return
        
        method, path, _ = parts
        
        if method == 'GET' and path == '/':
            self.handle_get_request(client_socket)
        elif method == 'POST' and path == '/add':
            if "\r\n\r\n" in request_data:
                headers, body = request_data.split("\r\n\r\n", 1)
            else:
                body = ""
            
            post_data = parse_qs(body)
            self.handle_post_request(client_socket, post_data)
        else:
            self.send_response(client_socket, '404 Not Found', 'text/html', '<h1>404 Not Found</h1>')
        
        client_socket.close()

    def handle_get_request(self, client_socket):
        html_content = self.generate_html()
        self.send_response(client_socket, '200 OK', 'text/html', html_content)

    def handle_post_request(self, client_socket, post_data):
        discipline = post_data.get('discipline', [''])[0].strip()
        grade = post_data.get('grade', [''])[0].strip()
        
        if discipline and grade:
            with self.lock:
                self.grades[discipline] = grade
            self.send_redirect(client_socket, '/')
        else:
            error_msg = "Ошибка: не получены все данные."
            self.send_response(client_socket, '400 Bad Request', 'text/html', f'<h1>400 Bad Request</h1><p>{error_msg}</p>')

    def generate_html(self):
        html = """
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <title>Учет оценок</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                table { border-collapse: collapse; width: 100%; margin-top: 20px; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
            <h1>Система учета оценок</h1>
            <form method="POST" action="/add">
                <h2>Добавить новую оценку</h2>
                <div><label>Дисциплина:</label><input type="text" name="discipline" required></div>
                <div><label>Оценка:</label><input type="number" name="grade" min="1" max="5" required></div>
                <input type="submit" value="Добавить">
            </form>
            <h2>Список оценок</h2>
            <table><tr><th>Дисциплина</th><th>Оценка</th></tr>
        """
        
        with self.lock:
            for discipline, grade in self.grades.items():
                html += f"<tr><td>{discipline}</td><td>{grade}</td></tr>"
        
        html += "</table></body></html>"
        return html

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Веб-сервер запущен на http://{self.host}:{self.port}")
        
        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"Подключение от {client_address}")
                
                thread = threading.Thread(target=self.handle_request, args=(client_socket,))
                thread.daemon = True
                thread.start()
        except KeyboardInterrupt:
            print("\nОстановка сервера...")
        finally:
            self.server_socket.close()
### Вывод по заданию 5
Реализован полнофункциональный веб-сервер с поддержкой GET и POST запросов. Сервер корректно обрабатывает форму добавления оценок, сохраняет данные и отображает их в виде таблицы. Использование потоков обеспечивает возможность обработки нескольких одновременных подключений.

## Общий вывод по работе
В ходе практической работы успешно реализованы все пять заданий, что соответствует 100% выполнения:

- UDP-взаимодействие - освоены основы работы с датаграммами
- TCP-сервер для вычислений - реализована надежная передача данных с обработкой математических операций
- HTTP-сервер - изучены принципы работы веб-серверов на низком уровне
- Многопользовательский чат - освоено многопоточное программирование для обработки одновременных подключений
- Веб-сервер с формами - реализована обработка GET/POST запросов и динамическая генерация HTML
- Работа демонстрирует уверенное владение сетевым программированием на Python и умение реализовывать клиент-серверные приложения различной сложности. Все компоненты работают корректно и готовы к практическому использованию.
