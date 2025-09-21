#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Задание 5: Веб-сервер для обработки GET и POST HTTP-запросов
Сервер принимает и записывает информацию о дисциплине и оценке,
отдает информацию обо всех оценках в виде HTML-страницы
"""

import socket
import sys
import json
import urllib.parse
import threading
import time
from datetime import datetime

class WebServer:
    """Класс веб-сервера для обработки GET и POST запросов"""
    
    def __init__(self, host='localhost', port=8081):
        self.host = host
        self.port = port
        self.grades = []  # Хранение оценок в памяти
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
    def start(self):
        """Запуск веб-сервера"""
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(1)
            print(f"Сервер запущен на {self.host}:{self.port}")
            print(f"Откройте http://{self.host}:{self.port}/ в браузере")

            while True:
                client_socket, addr = self.server_socket.accept()
                print(f"Подключен клиент: {addr}")
                
                try:
                    request = client_socket.recv(1024).decode('utf-8')
                    self.handle_request(client_socket, request)
                except Exception as e:
                    print(f"Ошибка обработки запроса: {e}")
                finally:
                    client_socket.close()
                    
        except KeyboardInterrupt:
            print("\nСервер остановлен пользователем")
        except Exception as e:
            print(f"Ошибка сервера: {e}")
        finally:
            self.server_socket.close()
    
    def handle_request(self, client_socket, request):
        """Обработка HTTP запросов"""
        lines = request.split('\n')
        if not lines:
            return
            
        request_line = lines[0]
        parts = request_line.split()
        if len(parts) >= 3:
            method, path, version = parts[0], parts[1], parts[2]
            
            if method == 'GET' and path == '/':
                self.handle_get_grades(client_socket)
            elif method == 'POST' and path == '/add_grade':
                self.handle_post_grade(client_socket, request)
            else:
                self.send_404(client_socket)
        else:
            self.send_404(client_socket)
    
    def handle_get_grades(self, client_socket):
        """Обработка GET запроса - отображение всех оценок"""
        html = self.generate_grades_html()
        response = f"""HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: {len(html.encode('utf-8'))}
Connection: close

{html}"""
        client_socket.send(response.encode('utf-8'))
 
    def handle_post_grade(self, client_socket, request):
        """Обработка POST запроса - добавление новой оценки"""
        body_start = request.find('\r\n\r\n')
        if body_start == -1:
            body_start = request.find('\n\n')
            if body_start != -1:
                body_start += 2
        else:
            body_start += 4
            
        if body_start != -1:
            body = request[body_start:]
            data = urllib.parse.parse_qs(body)
          
            discipline = data.get('discipline', [''])[0]
            grade = data.get('grade', [''])[0]
            
            if discipline and grade:
                try:
                    grade_value = int(grade)
                    if 1 <= grade_value <= 5:
                        self.grades.append({
                            'discipline': discipline,
                            'grade': grade_value,
                            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        })
                        
                        response = """HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Connection: close

{"message": "Оценка добавлена успешно"}"""
                        print(f"Добавлена оценка: {discipline} - {grade}")
                    else:
                        response = """HTTP/1.1 400 Bad Request
Content-Type: application/json; charset=utf-8
Connection: close

{"error": "Оценка должна быть от 1 до 5"}"""
                except ValueError:
                    response = """HTTP/1.1 400 Bad Request
Content-Type: application/json; charset=utf-8
Connection: close

{"error": "Оценка должна быть числом"}"""
            else:
                response = """HTTP/1.1 400 Bad Request
Content-Type: application/json; charset=utf-8
Connection: close

{"error": "Необходимы поля discipline и grade"}"""
        else:
            response = """HTTP/1.1 400 Bad Request
Content-Type: application/json; charset=utf-8
Connection: close

{"error": "Пустое тело запроса"}"""
        
        client_socket.send(response.encode('utf-8'))
    
    def generate_grades_html(self):
        """Генерация HTML страницы с оценками"""
        html = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Система оценок</title>
</head>
<body>
    <div class="container">
        <h1>Система управления оценками</h1>
        
        <h2>Список оценок</h2>"""
        
        if self.grades:
            html += """
        <table>
            <tr>
                <th>Дисциплина</th>
                <th>Оценка</th>
                <th>Дата добавления</th>
            </tr>"""
            
            for grade in self.grades:
                html += f"""
            <tr>
                <td>{grade['discipline']}</td>
                <td>{grade['grade']}</td>
                <td>{grade['created_at']}</td>
            </tr>"""
            
            html += """
        </table>"""
        else:
            html += """
        <div class="empty">Оценок пока нет</div>"""
        
        html += """
        
        <h2>Добавить оценку</h2>
        <form method="POST" action="/add_grade">
            <p>
                <label for="discipline">Дисциплина:</label><br>
                <input type="text" id="discipline" name="discipline" required 
                       placeholder="Введите название дисциплины">
            </p>
            <p>
                <label for="grade">Оценка:</label><br>
                <input type="number" id="grade" name="grade" min="1" max="5" required 
                       placeholder="Введите оценку от 1 до 5">
            </p>
            <p>
                <button type="submit">Добавить оценку</button>
            </p>
        </form>
    </div>
</body>
</html>"""
        return html
    
    def send_404(self, client_socket):
        """Отправка ошибки 404"""
        response = """HTTP/1.1 404 Not Found
Content-Type: text/html; charset=utf-8
Connection: close

<!DOCTYPE html>
<html>
<head>
    <title>404 Not Found</title>
    <meta charset="utf-8">
</head>
<body>
    <h1>404 Not Found</h1>
    <p>Запрашиваемая страница не найдена</p>
</body>
</html>"""
        client_socket.send(response.encode('utf-8'))

def run_demo():
    server = WebServer()
    server_thread = threading.Thread(target=server.start, daemon=True)
    server_thread.start()
    
    time.sleep(2)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nДемонстрация завершена")

if __name__ == "__main__":
    run_demo()