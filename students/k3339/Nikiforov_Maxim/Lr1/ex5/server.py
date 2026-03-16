import socket
import sys
import signal
import re
from urllib.parse import parse_qs, urlparse

class SimpleHTTPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.grades = {}  # здесь храним огценки
        self.running = True  # флаг для graceful shutdown
        
    def start_server(self):
        # создание и настройка серверного сокета
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        
        print(f"Сервер запущен на {self.host}:{self.port}")
        print("Нажмите Ctrl+C для остановки сервера")
        
        while self.running:
            try:
                # ожидание подключения клиента с таймаутом
                server_socket.settimeout(1.0)
                client_socket, address = server_socket.accept()
                print(f"Подключение от {address}")
                
                try:
                    # обработка запроса от клиента
                    self.handle_request(client_socket)
                except Exception as e:
                    print(f"Ошибка при обработке запроса: {e}")
                finally:
                    client_socket.close()
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    print(f"Ошибка сервера: {e}")
        
        server_socket.close()
        print("Сервер остановлен")
    
    def handle_request(self, client_socket):
        # чтение http запроса
        request_data = client_socket.recv(1024).decode('utf-8')
        if not request_data:
            return
            
        print("Получен запрос:")
        print(request_data)
        
        # парсинг http запроса
        lines = request_data.split('\n')
        request_line = lines[0]
        method, path, version = request_line.split()
        
        # обработка различных типов запросов
        if method == 'GET':
            self.handle_get(client_socket, path)
        elif method == 'POST':
            # читаем тело post запроса
            body_start = request_data.find('\r\n\r\n')
            if body_start != -1:
                body = request_data[body_start + 4:]
                self.handle_post(client_socket, body)
        else:
            self.send_error_response(client_socket, 405, "Method Not Allowed")
    
    def handle_get(self, client_socket, path):
        # обработка get запросов
        if path == '/':
            # отображаем главную страницу с формой и списком оценок
            self.send_main_page(client_socket)
        else:
            self.send_error_response(client_socket, 404, "Not Found")
    
    def handle_post(self, client_socket, body):
        # обработка post запросов для добавления оценок
        try:
            # парсим данные формы
            form_data = parse_qs(body)
            subject = form_data.get('subject', [''])[0].strip()
            grade = form_data.get('grade', [''])[0].strip()
            
            # валидация введенных данных
            validation_error = self.validate_input(subject, grade)
            if validation_error:
                self.send_error_response(client_socket, 400, validation_error)
                return
            
            # добавление новой оценки
            self.grades[subject] = grade
            print(f"Добавлена оценка: {subject} - {grade}")
            
            # перенаправляем на главную страницу
            self.send_redirect_response(client_socket, '/')
        except Exception as e:
            print(f"Ошибка при обработке POST: {e}")
            self.send_error_response(client_socket, 500, "Internal Server Error")
    
    def validate_input(self, subject, grade):
        if not subject:
            return "Дисциплина не может быть пустой"
        
        if len(subject) > 100:
            return "Название дисциплины слишком длинное (максимум 100 символов)"
        
        # проверка на недопустимые символы
        if not re.match(r'^[а-яА-Яa-zA-Z0-9\s\-\.]+$', subject):
            return "Название дисциплины содержит недопустимые символы"
        
        if not grade:
            return "Оценка не может быть пустой"
        
        try:
            grade_num = int(grade)
            if grade_num < 1 or grade_num > 5:
                return "Оценка должна быть от 1 до 5"
        except ValueError:
            return "Оценка должна быть числом"
        
        return None  # валидация прошла успешно
    
    def send_main_page(self, client_socket):
        # отправка главной страницы с формой и списком оценок
        html_content = self.render_template()
        
        response = f"""HTTP/1.1 200 OK\r
Content-Type: text/html; charset=utf-8\r
Content-Length: {len(html_content.encode('utf-8'))}\r
\r
{html_content}"""
        
        client_socket.send(response.encode('utf-8'))
    
    def render_template(self):
        # чтение html из файла и подстановка оценок
        try:
            with open('template.html', 'r', encoding='utf-8') as file:
                template = file.read()
        except FileNotFoundError:
            template = '<html><body><h1>шаблон не найден</h1>{{grades}}</body></html>'

        grades_html = ''
        if self.grades:
            for subject, grade in self.grades.items():
                grades_html += f'<div class="grade-item"><strong>{subject}</strong>: {grade}</div>'
        else:
            grades_html = '<p>Оценки пока не добавлены</p>'

        return template.replace('{{grades}}', grades_html)
    
    def send_redirect_response(self, client_socket, location):
        # отправка перенаправления
        response = f"""HTTP/1.1 302 Found\r
Location: {location}\r
Content-Length: 0\r
\r
"""
        client_socket.send(response.encode('utf-8'))
    
    def send_error_response(self, client_socket, status_code, message):
        # отправка ошибочного ответа
        html_content = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Ошибка {status_code}</title>
</head>
<body>
    <h1>Ошибка {status_code}</h1>
    <p>{message}</p>
    <a href="/">Вернуться на главную</a>
</body>
</html>"""
        
        response = f"""HTTP/1.1 {status_code} {message}\r
Content-Type: text/html; charset=utf-8\r
Content-Length: {len(html_content.encode('utf-8'))}\r
\r
{html_content}"""
        
        client_socket.send(response.encode('utf-8'))

def signal_handler(signum, frame):
    # обработчик сигнала для graceful shutdown
    print("\nПолучен сигнал остановки...")
    global server
    if 'server' in globals():
        server.running = False

def main():
    # запуск сервера
    if len(sys.argv) != 3:
        print("Использование: python server.py <host> <port>")
        print("Пример: python server.py localhost 8080")
        sys.exit(1)
    
    host = sys.argv[1]
    port = int(sys.argv[2])
    
    global server
    server = SimpleHTTPServer(host, port)
    
    # настройка обработчиков сигналов для graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\nСервер остановлен")

if __name__ == "__main__":
    main()
