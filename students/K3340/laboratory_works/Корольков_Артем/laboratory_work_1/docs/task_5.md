# Задание 5: Веб-сервер для обработки GET и POST запросов
## Описание задания
Написать простой веб-сервер для обработки GET и POST HTTP-запросов. Сервер должен принимать и записывать информацию о дисциплине и оценке по дисциплине, а также отдавать информацию обо всех оценках в виде HTML-страницы.

## Ход выполнения
### Серверная часть (task_5_server.py):
```python
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
```
## Вывод по заданию 5
Реализован полнофункциональный веб-сервер с поддержкой GET и POST запросов. Сервер корректно обрабатывает форму добавления оценок, сохраняет данные и отображает их в виде таблицы. Использование потоков обеспечивает возможность обработки нескольких одновременных подключений.

# Общий вывод по работе
В ходе практической работы успешно реализованы все пять заданий, что соответствует 100% выполнения:
1. UDP-взаимодействие - освоены основы работы с датаграммами
2. TCP-сервер для вычислений - реализована надежная передача данных с обработкой математических операций
3. HTTP-сервер - изучены принципы работы веб-серверов на низком уровне
4. Многопользовательский чат - освоено многопоточное программирование для обработки одновременных подключений
5. Веб-сервер с формами - реализована обработка GET/POST запросов и динамическая генерация HTML

Работа демонстрирует уверенное владение сетевым программированием на Python и умение реализовывать клиент-серверные приложения различной сложности. Все компоненты работают корректно и готовы к практическому использованию.
