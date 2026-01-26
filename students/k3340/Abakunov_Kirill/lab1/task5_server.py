#!/usr/bin/env python3
"""
Задание 5: Веб-сервер для обработки GET и POST запросов
Принимает информацию о дисциплинах и оценках, отображает их в HTML
"""

import socket
import urllib.parse

# Хранилище оценок (дисциплина: оценка)
grades = {}

def parse_request(request):
    """Парсит HTTP-запрос"""
    lines = request.split('\r\n')
    if not lines:
        return None, None, None
    
    # Парсим первую строку (метод, путь, протокол)
    first_line = lines[0].split()
    if len(first_line) < 3:
        return None, None, None
    
    method = first_line[0]
    path = first_line[1]
    
    # Парсим заголовки
    headers = {}
    body_start = 0
    for i, line in enumerate(lines[1:], 1):
        if line == '':
            body_start = i + 1
            break
        if ':' in line:
            key, value = line.split(':', 1)
            headers[key.strip()] = value.strip()
    
    # Получаем тело запроса
    body = '\r\n'.join(lines[body_start:]) if body_start > 0 else ''
    
    return method, path, body

def generate_html_page():
    """Генерирует HTML-страницу с формой и таблицей оценок"""
    html = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Журнал оценок</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 40px;
            animation: fadeIn 0.5s ease-in;
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        h1 {
            color: #667eea;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }
        
        .form-section {
            background: #f8f9fa;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            border-left: 5px solid #667eea;
        }
        
        .form-section h2 {
            color: #333;
            margin-bottom: 20px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            color: #555;
            margin-bottom: 8px;
            font-weight: 600;
        }
        
        input[type="text"],
        input[type="number"] {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        input[type="text"]:focus,
        input[type="number"]:focus {
            outline: none;
            border-color: #667eea;
        }
        
        button {
            background: #667eea;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.3s, transform 0.1s;
            width: 100%;
        }
        
        button:hover {
            background: #5568d3;
            transform: translateY(-2px);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        .grades-section {
            margin-top: 30px;
        }
        
        .grades-section h2 {
            color: #333;
            margin-bottom: 20px;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }
        
        th {
            background: #667eea;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }
        
        td {
            padding: 15px;
            border-bottom: 1px solid #eee;
            color: #555;
        }
        
        tr:last-child td {
            border-bottom: none;
        }
        
        tr:hover {
            background: #f8f9fa;
        }
        
        .empty-state {
            text-align: center;
            padding: 40px;
            color: #999;
            font-style: italic;
        }
        
        .stats {
            display: flex;
            justify-content: space-around;
            margin-top: 20px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        
        .stat-item {
            text-align: center;
        }
        
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        
        .stat-label {
            color: #666;
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 Журнал оценок</h1>
        <p class="subtitle">Лабораторная работа №1 - Задание 5</p>
        
        <div class="form-section">
            <h2>Добавить оценку</h2>
            <form method="POST" action="/">
                <div class="form-group">
                    <label for="subject">Дисциплина:</label>
                    <input type="text" id="subject" name="subject" required 
                           placeholder="Например: Сетевое программирование">
                </div>
                <div class="form-group">
                    <label for="grade">Оценка (2-5):</label>
                    <input type="number" id="grade" name="grade" min="2" max="5" required
                           placeholder="Введите оценку от 2 до 5">
                </div>
                <button type="submit">Добавить оценку</button>
            </form>
        </div>
        
        <div class="grades-section">
            <h2>Список оценок</h2>
"""
    
    if grades:
        # Вычисляем статистику
        total_subjects = len(grades)
        average_grade = sum(grades.values()) / total_subjects if total_subjects > 0 else 0
        
        html += f"""
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-value">{total_subjects}</div>
                    <div class="stat-label">Дисциплин</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">{average_grade:.2f}</div>
                    <div class="stat-label">Средний балл</div>
                </div>
            </div>
            
            <table>
                <thead>
                    <tr>
                        <th>№</th>
                        <th>Дисциплина</th>
                        <th>Оценка</th>
                    </tr>
                </thead>
                <tbody>
"""
        for idx, (subject, grade) in enumerate(grades.items(), 1):
            html += f"""
                    <tr>
                        <td>{idx}</td>
                        <td>{subject}</td>
                        <td>{grade}</td>
                    </tr>
"""
        html += """
                </tbody>
            </table>
"""
    else:
        html += """
            <div class="empty-state">
                <p>Пока нет добавленных оценок</p>
                <p>Используйте форму выше для добавления первой оценки</p>
            </div>
"""
    
    html += """
        </div>
    </div>
</body>
</html>
"""
    return html

def handle_get_request():
    """Обрабатывает GET-запрос"""
    html = generate_html_page()
    
    response = "HTTP/1.1 200 OK\r\n"
    response += "Content-Type: text/html; charset=utf-8\r\n"
    response += f"Content-Length: {len(html.encode('utf-8'))}\r\n"
    response += "Connection: close\r\n"
    response += "\r\n"
    response += html
    
    return response

def handle_post_request(body):
    """Обрабатывает POST-запрос"""
    try:
        # Парсим данные формы
        params = urllib.parse.parse_qs(body)
        
        if 'subject' in params and 'grade' in params:
            subject = params['subject'][0]
            grade = int(params['grade'][0])
            
            # Валидация
            if 2 <= grade <= 5:
                grades[subject] = grade
                print(f"[+] Добавлена оценка: {subject} = {grade}")
            else:
                print(f"[!] Неверная оценка: {grade}")
        
    except Exception as e:
        print(f"[!] Ошибка обработки POST-запроса: {e}")
    
    # Возвращаем редирект на главную страницу
    response = "HTTP/1.1 303 See Other\r\n"
    response += "Location: /\r\n"
    response += "Connection: close\r\n"
    response += "\r\n"
    
    return response

def main():
    # Создаем TCP сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Позволяем переиспользовать адрес
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Настройки сервера
    host = 'localhost'
    port = 8000
    
    # Привязываем сокет к адресу и порту
    server_socket.bind((host, port))
    
    # Начинаем прослушивание
    server_socket.listen(5)
    
    print("=" * 60)
    print(f"Веб-сервер для журнала оценок запущен")
    print(f"Откройте в браузере: http://{host}:{port}")
    print("=" * 60)
    print("Для остановки нажмите Ctrl+C\n")
    
    try:
        while True:
            # Принимаем подключение
            client_socket, client_address = server_socket.accept()
            
            try:
                # Получаем HTTP-запрос
                request = client_socket.recv(4096).decode('utf-8')
                
                # Парсим запрос
                method, path, body = parse_request(request)
                
                print(f"[{method}] {path} от {client_address}")
                
                # Обрабатываем запрос
                if method == 'GET':
                    response = handle_get_request()
                elif method == 'POST':
                    response = handle_post_request(body)
                else:
                    response = "HTTP/1.1 405 Method Not Allowed\r\n\r\n"
                
                # Отправляем ответ
                client_socket.send(response.encode('utf-8'))
                
            except Exception as e:
                print(f"[!] Ошибка обработки запроса: {e}")
                error_response = "HTTP/1.1 500 Internal Server Error\r\n\r\n"
                client_socket.send(error_response.encode('utf-8'))
            
            finally:
                client_socket.close()
    
    except KeyboardInterrupt:
        print("\n\nОстановка сервера...")
    finally:
        server_socket.close()
        print("Сервер остановлен")

if __name__ == "__main__":
    main()
