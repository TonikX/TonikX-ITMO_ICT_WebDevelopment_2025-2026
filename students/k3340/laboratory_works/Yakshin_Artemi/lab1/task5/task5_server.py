#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Задание 5: Веб-сервер для обработки GET и POST запросов
Сервер принимает информацию о дисциплинах и оценках
"""

import socket
import json
import urllib.parse
import os
from datetime import datetime

class GradeServer:
    def __init__(self, host='localhost', port=8081):
        self.host = host
        self.port = port
        self.grades = []  # Список для хранения оценок
        # Определяем путь к файлу оценок относительно директории скрипта
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.grades_file = os.path.join(script_dir, 'grades.json')
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Загружаем сохраненные оценки при запуске
        self.load_grades()
    
    def load_grades(self):
        """Загружает оценки из файла"""
        try:
            print(f"Пытаемся загрузить оценки из файла: {self.grades_file}")
            if os.path.exists(self.grades_file):
                with open(self.grades_file, 'r', encoding='utf-8') as file:
                    self.grades = json.load(file)
                print(f"Загружено {len(self.grades)} оценок из файла")
            else:
                print(f"Файл оценок не найден: {self.grades_file}")
                print("Начинаем с пустого списка")
        except Exception as e:
            print(f"Ошибка при загрузке оценок: {e}")
            self.grades = []
    
    def save_grades(self):
        """Сохраняет оценки в файл"""
        try:
            with open(self.grades_file, 'w', encoding='utf-8') as file:
                json.dump(self.grades, file, ensure_ascii=False, indent=2)
            print(f"Сохранено {len(self.grades)} оценок в файл: {self.grades_file}")
        except Exception as e:
            print(f"Ошибка при сохранении оценок: {e}")
        
    def start_server(self):
        """Запускает сервер"""
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Веб-сервер запущен на http://{self.host}:{self.port}")
        print("Ожидание запросов...")
        
        try:
            while True:
                client_socket, address = self.server_socket.accept()
                print(f"Подключен клиент: {address}")
                
                try:
                    self.handle_request(client_socket)
                except Exception as e:
                    print(f"Ошибка при обработке запроса: {e}")
                finally:
                    client_socket.close()
                    
        except KeyboardInterrupt:
            print("\nСервер остановлен")
        finally:
            self.server_socket.close()
    
    def handle_request(self, client_socket):
        """Обрабатывает HTTP запрос"""
        request = client_socket.recv(4096).decode('utf-8')
        print(f"Получен запрос:\n{request[:200]}...")
        
        # Парсим HTTP запрос
        lines = request.split('\n')
        if not lines:
            return
            
        request_line = lines[0]
        method, path, _ = request_line.split(' ', 2)
        
        if method == 'GET':
            if path == '/':
                response = self.get_grades_page()
            elif path == '/style.css':
                response = self.get_css_file()
            elif path == '/api/grades':
                response = self.get_grades_api()
            else:
                print(f"404 ошибка для пути: {path}")
                response = self.get_404_response()
        elif method == 'POST':
            if path == '/api/grades':
                response = self.post_grades(request)
            else:
                response = self.get_404_response()
        else:
            response = self.get_405_response()
        
        client_socket.send(response.encode('utf-8'))
    
    def get_grades_page(self):
        """Возвращает HTML страницу с оценками"""
        grades_html = self.generate_grades_html()
        html_content = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Система оценок</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>Система управления оценками</h1>
        
        <div class="form-section">
            <h2>Добавить оценку</h2>
            <form id="gradeForm">
                <div class="form-group">
                    <label for="discipline">Дисциплина:</label>
                    <input type="text" id="discipline" name="discipline" required>
                </div>
                <div class="form-group">
                    <label for="grade">Оценка:</label>
                    <select id="grade" name="grade" required>
                        <option value="">Выберите оценку</option>
                        <option value="5">5 (Отлично)</option>
                        <option value="4">4 (Хорошо)</option>
                        <option value="3">3 (Удовлетворительно)</option>
                        <option value="2">2 (Неудовлетворительно)</option>
                    </select>
                </div>
                <button type="submit">Добавить оценку</button>
            </form>
        </div>
        
        <div class="form-section">
            <h2>Все оценки</h2>
            <div id="gradesList">
                """ + grades_html + """
            </div>
        </div>
    </div>
    
        <script>
        document.getElementById('gradeForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const data = Object.fromEntries(formData);
            
            fetch('/api/grades', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams(data)
            })
            .then(response => response.text())
            .then(result => {
                alert('Оценка добавлена!');
                location.reload();
            })
            .catch(error => {
                alert('Ошибка: ' + error);
            });
        });
    </script>
</body>
</html>"""
        
        response = f"""HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: {len(html_content.encode('utf-8'))}
Connection: close
Server: Python Grade Server

{html_content}"""
        return response
    
    def get_css_file(self):
        """Возвращает CSS файл"""
        import os
        # Определяем путь к CSS файлу относительно скрипта
        script_dir = os.path.dirname(os.path.abspath(__file__))
        css_file = os.path.join(script_dir, 'style.css')
        
        try:
            with open(css_file, 'r', encoding='utf-8') as file:
                css_content = file.read()
        except FileNotFoundError:
            css_content = "/* CSS файл не найден */"
        except Exception as e:
            css_content = f"/* Ошибка загрузки CSS: {str(e)} */"
        
        response = f"""HTTP/1.1 200 OK
Content-Type: text/css; charset=utf-8
Content-Length: {len(css_content.encode('utf-8'))}
Connection: close
Server: Python Grade Server

{css_content}"""
        return response
    
    def get_grades_api(self):
        """Возвращает JSON с оценками"""
        grades_json = json.dumps(self.grades, ensure_ascii=False, indent=2)
        response = f"""HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: {len(grades_json.encode('utf-8'))}
Connection: close
Server: Python Grade Server

{grades_json}"""
        return response
    
    def post_grades(self, request):
        """Обрабатывает POST запрос для добавления оценки"""
        try:
            # Извлекаем данные из тела запроса
            body_start = request.find('\r\n\r\n')
            if body_start == -1:
                return self.get_400_response()
            
            body = request[body_start + 4:]
            parsed_data = urllib.parse.parse_qs(body)
            
            discipline = parsed_data.get('discipline', [''])[0]
            grade = parsed_data.get('grade', [''])[0]
            
            if not discipline or not grade:
                return self.get_400_response()
            
            # Добавляем оценку
            grade_entry = {
                'discipline': discipline,
                'grade': int(grade),
                'timestamp': datetime.now().isoformat()
            }
            self.grades.append(grade_entry)
            
            # Сохраняем оценки в файл
            self.save_grades()
            
            response_body = f"Оценка добавлена: {discipline} - {grade}"
            response = f"""HTTP/1.1 200 OK
Content-Type: text/plain; charset=utf-8
Content-Length: {len(response_body.encode('utf-8'))}
Connection: close
Server: Python Grade Server

{response_body}"""
            return response
            
        except Exception as e:
            return self.get_500_response(str(e))
    
    def generate_grades_html(self):
        """Генерирует HTML таблицу с оценками"""
        if not self.grades:
            return "<p>Оценок пока нет</p>"
        
        html = "<table class='grades-table'>"
        html += "<tr><th>Дисциплина</th><th>Оценка</th><th>Дата</th></tr>"
        
        for grade in self.grades:
            timestamp = datetime.fromisoformat(grade['timestamp']).strftime('%d.%m.%Y %H:%M')
            html += f"<tr><td>{grade['discipline']}</td><td>{grade['grade']}</td><td>{timestamp}</td></tr>"
        
        html += "</table>"
        return html
    
    def get_404_response(self):
        """Возвращает 404 ошибку"""
        content = "<html><body><h1>404 Not Found</h1></body></html>"
        return f"""HTTP/1.1 404 Not Found
Content-Type: text/html
Content-Length: {len(content)}
Connection: close

{content}"""
    
    def get_400_response(self):
        """Возвращает 400 ошибку"""
        content = "<html><body><h1>400 Bad Request</h1></body></html>"
        return f"""HTTP/1.1 400 Bad Request
Content-Type: text/html
Content-Length: {len(content)}
Connection: close

{content}"""
    
    def get_405_response(self):
        """Возвращает 405 ошибку"""
        content = "<html><body><h1>405 Method Not Allowed</h1></body></html>"
        return f"""HTTP/1.1 405 Method Not Allowed
Content-Type: text/html
Content-Length: {len(content)}
Connection: close

{content}"""
    
    def get_500_response(self, error):
        """Возвращает 500 ошибку"""
        content = f"<html><body><h1>500 Internal Server Error</h1><p>{error}</p></body></html>"
        return f"""HTTP/1.1 500 Internal Server Error
Content-Type: text/html
Content-Length: {len(content)}
Connection: close

{content}"""

def main():
    server = GradeServer()
    server.start_server()

if __name__ == "__main__":
    main()
