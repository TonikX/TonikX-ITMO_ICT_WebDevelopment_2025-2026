#!/usr/bin/env python3
"""
Web Server для задания 5
Веб-сервер для обработки GET и POST HTTP-запросов
Принимает и записывает информацию о дисциплине и оценке
Отдает информацию обо всех оценках в виде HTML-страницы
"""

import socket
import sys
import os
import urllib.parse
from datetime import datetime

class GradeManager:
    """Класс для управления оценками"""
    
    def __init__(self):
        self.grades_file = "grades.txt"
        self.grades = []
        self.load_grades()
    
    def load_grades(self):
        """Загружает оценки из файла"""
        try:
            if os.path.exists(self.grades_file):
                with open(self.grades_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            parts = line.split('|')
                            if len(parts) == 3:
                                self.grades.append({
                                    'discipline': parts[0],
                                    'grade': parts[1],
                                    'timestamp': parts[2]
                                })
        except Exception as e:
            print(f"Ошибка загрузки оценок: {e}")
    
    def save_grades(self):
        """Сохраняет оценки в файл"""
        try:
            with open(self.grades_file, 'w', encoding='utf-8') as f:
                for grade in self.grades:
                    f.write(f"{grade['discipline']}|{grade['grade']}|{grade['timestamp']}\n")
        except Exception as e:
            print(f"Ошибка сохранения оценок: {e}")
    
    def add_grade(self, discipline, grade):
        """Добавляет новую оценку"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.grades.append({
            'discipline': discipline,
            'grade': grade,
            'timestamp': timestamp
        })
        self.save_grades()
        return True
    
    def get_all_grades(self):
        """Возвращает все оценки"""
        return self.grades

class WebServer:
    """Веб-сервер для обработки GET и POST запросов"""
    
    def __init__(self, host='localhost', port=8081):
        self.host = host
        self.port = port
        self.grade_manager = GradeManager()
        self.server_socket = None
    
    def start(self):
        """Запускает веб-сервер"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            
            print(f"🌐 Web Server запущен на http://{self.host}:{self.port}")
            print("Доступные эндпоинты:")
            print("  GET  / - показать все оценки")
            print("  POST /add - добавить новую оценку")
            print("Нажмите Ctrl+C для остановки сервера")
            print("-" * 50)
            
            while True:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    print(f"📱 Подключение от {client_address}")
                    
                    # Обрабатываем запрос
                    self.handle_request(client_socket, client_address)
                    
                except socket.error:
                    break
                except Exception as e:
                    print(f"Ошибка обработки подключения: {e}")
        
        except KeyboardInterrupt:
            print("\n🛑 Сервер остановлен пользователем")
        except Exception as e:
            print(f"Ошибка сервера: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """Останавливает сервер"""
        if self.server_socket:
            self.server_socket.close()
        print("🛑 Сервер завершил работу")
    
    def handle_request(self, client_socket, client_address):
        """Обрабатывает HTTP-запрос"""
        try:
            # Получаем запрос
            request = client_socket.recv(4096).decode('utf-8')
            if not request:
                return
            
            # Парсим запрос
            lines = request.split('\n')
            if not lines:
                return
            
            request_line = lines[0].strip()
            parts = request_line.split()
            
            if len(parts) < 3:
                self.send_error_response(client_socket, 400, "Bad Request")
                return
            
            method, path, version = parts[0], parts[1], parts[2]
            
            print(f"📝 {method} {path} от {client_address}")
            
            # Обрабатываем запрос в зависимости от метода
            if method == 'GET':
                self.handle_get(client_socket, path)
            elif method == 'POST':
                self.handle_post(client_socket, path, request)
            else:
                self.send_error_response(client_socket, 405, "Method Not Allowed")
        
        except Exception as e:
            print(f"Ошибка обработки запроса: {e}")
            self.send_error_response(client_socket, 500, "Internal Server Error")
        finally:
            client_socket.close()
    
    def handle_get(self, client_socket, path):
        """Обрабатывает GET-запросы"""
        if path == '/' or path == '/index.html':
            # Показываем все оценки
            html_content = self.generate_grades_html()
            self.send_html_response(client_socket, html_content)
        else:
            self.send_error_response(client_socket, 404, "Not Found")
    
    def handle_post(self, client_socket, path, request):
        """Обрабатывает POST-запросы"""
        if path == '/add':
            # Добавляем новую оценку
            try:
                # Извлекаем данные из POST-запроса
                body = self.extract_post_body(request)
                discipline, grade = self.parse_form_data(body)
                
                if discipline and grade:
                    self.grade_manager.add_grade(discipline, grade)
                    print(f"✅ Добавлена оценка: {discipline} - {grade}")
                    
                    # Перенаправляем на главную страницу
                    self.send_redirect_response(client_socket, "/")
                else:
                    self.send_error_response(client_socket, 400, "Bad Request - Missing data")
            
            except Exception as e:
                print(f"Ошибка добавления оценки: {e}")
                self.send_error_response(client_socket, 500, "Internal Server Error")
        else:
            self.send_error_response(client_socket, 404, "Not Found")
    
    def extract_post_body(self, request):
        """Извлекает тело POST-запроса"""
        try:
            # Находим пустую строку, которая разделяет заголовки и тело
            parts = request.split('\r\n\r\n')
            if len(parts) > 1:
                return parts[1]
            return ""
        except:
            return ""
    
    def parse_form_data(self, body):
        """Парсит данные формы"""
        try:
            data = urllib.parse.parse_qs(body)
            discipline = data.get('discipline', [''])[0]
            grade = data.get('grade', [''])[0]
            return discipline, grade
        except:
            return None, None
    
    def generate_grades_html(self):
        """Генерирует HTML-страницу с оценками"""
        grades = self.grade_manager.get_all_grades()
        
        html = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Система оценок - Задание 5</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            padding: 40px;
        }}
        
        h1 {{
            color: #333;
            text-align: center;
            margin-bottom: 30px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .form-section {{
            background: #f8f9fa;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            border-left: 4px solid #667eea;
        }}
        
        .form-group {{
            margin-bottom: 20px;
        }}
        
        label {{
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #333;
        }}
        
        input[type="text"], input[type="number"] {{
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            box-sizing: border-box;
        }}
        
        input[type="text"]:focus, input[type="number"]:focus {{
            outline: none;
            border-color: #667eea;
        }}
        
        button {{
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: transform 0.2s;
        }}
        
        button:hover {{
            transform: translateY(-2px);
        }}
        
        .grades-section {{
            background: #f8f9fa;
            padding: 30px;
            border-radius: 15px;
            border-left: 4px solid #28a745;
        }}
        
        .grades-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        
        .grades-table th, .grades-table td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        
        .grades-table th {{
            background: #667eea;
            color: white;
            font-weight: bold;
        }}
        
        .grades-table tr:nth-child(even) {{
            background: #f2f2f2;
        }}
        
        .grades-table tr:hover {{
            background: #e9ecef;
        }}
        
        .no-grades {{
            text-align: center;
            color: #666;
            font-style: italic;
            padding: 20px;
        }}
        
        .stats {{
            display: flex;
            justify-content: space-around;
            margin: 20px 0;
            padding: 20px;
            background: #e9ecef;
            border-radius: 10px;
        }}
        
        .stat-item {{
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        
        .stat-label {{
            color: #666;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 Система оценок</h1>
        
        <div class="form-section">
            <h2>➕ Добавить новую оценку</h2>
            <form action="/add" method="POST">
                <div class="form-group">
                    <label for="discipline">Дисциплина:</label>
                    <input type="text" id="discipline" name="discipline" required 
                           placeholder="Например: Математика, Физика, Программирование">
                </div>
                <div class="form-group">
                    <label for="grade">Оценка:</label>
                    <input type="number" id="grade" name="grade" min="1" max="5" required 
                           placeholder="От 1 до 5">
                </div>
                <button type="submit">Добавить оценку</button>
            </form>
        </div>
        
        <div class="grades-section">
            <h2>📊 Все оценки</h2>
"""
        
        if grades:
            # Статистика
            total_grades = len(grades)
            avg_grade = sum(int(g['grade']) for g in grades) / total_grades
            disciplines = len(set(g['discipline'] for g in grades))
            
            html += f"""
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-number">{total_grades}</div>
                    <div class="stat-label">Всего оценок</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{avg_grade:.1f}</div>
                    <div class="stat-label">Средний балл</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{disciplines}</div>
                    <div class="stat-label">Дисциплин</div>
                </div>
            </div>
            
            <table class="grades-table">
                <thead>
                    <tr>
                        <th>Дисциплина</th>
                        <th>Оценка</th>
                        <th>Дата и время</th>
                    </tr>
                </thead>
                <tbody>
"""
            
            for grade in reversed(grades):  # Показываем последние оценки первыми
                html += f"""
                    <tr>
                        <td>{grade['discipline']}</td>
                        <td>{grade['grade']}</td>
                        <td>{grade['timestamp']}</td>
                    </tr>
"""
            
            html += """
                </tbody>
            </table>
"""
        else:
            html += """
            <div class="no-grades">
                📝 Пока нет оценок. Добавьте первую оценку выше!
            </div>
"""
        
        html += """
        </div>
    </div>
</body>
</html>
"""
        
        return html
    
    def send_html_response(self, client_socket, html_content):
        """Отправляет HTML-ответ"""
        response = f"""HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: {len(html_content.encode('utf-8'))}
Server: Python-Web-Server/1.0
Date: {datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')}
Connection: close

{html_content}"""
        
        client_socket.send(response.encode('utf-8'))
    
    def send_redirect_response(self, client_socket, location):
        """Отправляет редирект"""
        response = f"""HTTP/1.1 302 Found
Location: {location}
Server: Python-Web-Server/1.0
Date: {datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')}
Connection: close

"""
        
        client_socket.send(response.encode('utf-8'))
    
    def send_error_response(self, client_socket, status_code, message):
        """Отправляет ответ с ошибкой"""
        status_messages = {
            400: "Bad Request",
            404: "Not Found",
            405: "Method Not Allowed",
            500: "Internal Server Error"
        }
        
        error_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{status_code} - {status_messages.get(status_code, 'Error')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; text-align: center; margin-top: 100px; }}
        h1 {{ color: #e74c3c; }}
    </style>
</head>
<body>
    <h1>{status_code} - {message}</h1>
    <p><a href="/">Вернуться на главную</a></p>
</body>
</html>"""
        
        response = f"""HTTP/1.1 {status_code} {status_messages.get(status_code, 'Error')}
Content-Type: text/html; charset=utf-8
Content-Length: {len(error_html.encode('utf-8'))}
Server: Python-Web-Server/1.0
Date: {datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')}
Connection: close

{error_html}"""
        
        client_socket.send(response.encode('utf-8'))

def main():
    server = WebServer()
    
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n🛑 Получен сигнал остановки...")
        server.stop()
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        server.stop()
        sys.exit(1)

if __name__ == "__main__":
    main()
