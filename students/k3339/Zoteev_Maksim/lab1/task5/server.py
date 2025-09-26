import socket
import urllib.parse
from collections import defaultdict

# Структурированное хранение оценок по дисциплинам
# Ключ - название дисциплины, значение - список оценок
grades_journal = defaultdict(list)

def parse_http_request(request_data):
    """Парсит HTTP запрос и возвращает метод, путь и тело запроса"""
    lines = request_data.split('\r\n')
    if not lines:
        return None, None, None
    
    # Парсим первую строку (request line)
    request_line = lines[0]
    parts = request_line.split(' ')
    if len(parts) < 2:
        return None, None, None
    
    method = parts[0]
    path = parts[1]
    
    # Ищем тело запроса (после пустой строки)
    body = ""
    empty_line_found = False
    for line in lines:
        if empty_line_found:
            body += line + '\r\n'
        elif line == "":
            empty_line_found = True
    
    return method, path, body.strip()

def create_html_response(html_content):
    """Создает HTTP ответ с HTML контентом"""
    response_body = html_content.encode('utf-8')
    response_headers = f"""HTTP/1.1 200 OK\r
Content-Type: text/html; charset=utf-8\r
Content-Length: {len(response_body)}\r
Connection: close\r
\r
"""
    return response_headers.encode('utf-8') + response_body

def create_redirect_response(location):
    """Создает HTTP ответ-редирект"""
    response = f"""HTTP/1.1 302 Found\r
Location: {location}\r
Connection: close\r
\r
"""
    return response.encode('utf-8')

def generate_main_page():
    """Генерирует главную HTML страницу с формой и таблицей оценок"""
    html = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Журнал оценок</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .form-section {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #555;
        }
        input[type="text"], input[type="number"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
            box-sizing: border-box;
        }
        button {
            background-color: #007bff;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s;
        }
        button:hover {
            background-color: #0056b3;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f8f9fa;
            font-weight: bold;
            color: #333;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        .no-data {
            text-align: center;
            color: #666;
            font-style: italic;
            padding: 20px;
        }
        .grades-list {
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
        }
        .grade-item {
            background-color: #e9ecef;
            padding: 4px 8px;
            border-radius: 3px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 Журнал оценок по дисциплинам</h1>
        
        <div class="form-section">
            <h2>Добавить оценку</h2>
            <form method="POST" action="/add_grade">
                <div class="form-group">
                    <label for="discipline">Дисциплина:</label>
                    <input type="text" id="discipline" name="discipline" required>
                </div>
                <div class="form-group">
                    <label for="grade">Оценка (1-5):</label>
                    <input type="number" id="grade" name="grade" min="1" max="5" required>
                </div>
                <button type="submit">Добавить оценку</button>
            </form>
        </div>
        
        <h2>Все оценки</h2>
        """
    
    if grades_journal:
        html += """
        <table>
            <thead>
                <tr>
                    <th>Дисциплина</th>
                    <th>Оценки</th>
                    <th>Количество оценок</th>
                    <th>Средний балл</th>
                </tr>
            </thead>
            <tbody>
        """
        
        for discipline, grades in sorted(grades_journal.items()):
            avg_grade = sum(grades) / len(grades)
            grades_html = ''.join([f'<span class="grade-item">{grade}</span>' for grade in grades])
            
            html += f"""
                <tr>
                    <td><strong>{discipline}</strong></td>
                    <td><div class="grades-list">{grades_html}</div></td>
                    <td>{len(grades)}</td>
                    <td>{avg_grade:.2f}</td>
                </tr>
            """
        
        html += """
            </tbody>
        </table>
        """
    else:
        html += '<div class="no-data">Пока нет добавленных оценок. Добавьте первую оценку с помощью формы выше.</div>'
    
    html += """
    </div>
</body>
</html>
"""
    return html

def handle_get_request(path):
    """Обрабатывает GET запросы"""
    if path == "/" or path == "/index.html":
        return create_html_response(generate_main_page())
    else:
        # 404 Not Found
        not_found_html = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>404 - Страница не найдена</title>
</head>
<body>
    <h1>404 - Страница не найдена</h1>
    <p><a href="/">Вернуться на главную</a></p>
</body>
</html>"""
        response_body = not_found_html.encode('utf-8')
        response_headers = f"""HTTP/1.1 404 Not Found\r
Content-Type: text/html; charset=utf-8\r
Content-Length: {len(response_body)}\r
Connection: close\r
\r
"""
        return response_headers.encode('utf-8') + response_body

def handle_post_request(path, body):
    """Обрабатывает POST запросы"""
    if path == "/add_grade":
        # Парсим данные формы
        try:
            form_data = urllib.parse.parse_qs(body)
            discipline = form_data.get('discipline', [''])[0].strip()
            grade_str = form_data.get('grade', [''])[0].strip()
            
            if discipline and grade_str:
                grade = int(grade_str)
                if 1 <= grade <= 5:
                    # Добавляем оценку к дисциплине
                    grades_journal[discipline].append(grade)
                    print(f"Добавлена оценка {grade} по дисциплине '{discipline}'")
                    print(f"Текущие оценки по '{discipline}': {grades_journal[discipline]}")
                    
                    # Редирект на главную страницу
                    return create_redirect_response("/")
                else:
                    raise ValueError("Оценка должна быть от 1 до 5")
            else:
                raise ValueError("Не заполнены обязательные поля")
                
        except (ValueError, KeyError) as e:
            # Возвращаем страницу с ошибкой
            error_html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Ошибка</title>
</head>
<body>
    <h1>Ошибка при добавлении оценки</h1>
    <p>Ошибка: {str(e)}</p>
    <p><a href="/">Вернуться на главную</a></p>
</body>
</html>"""
            return create_html_response(error_html)
    
    # Если путь не найден
    return handle_get_request("/404")

def run_server(host='localhost', port=8080):
    """Запускает HTTP сервер"""
    # Создаем socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # Привязываем socket к адресу и порту
        server_socket.bind((host, port))
        server_socket.listen(5)
        
        print(f"🚀 Сервер запущен на http://{host}:{port}")
        print("Для остановки нажмите Ctrl+C")
        print("-" * 50)
        
        while True:
            # Принимаем подключение
            client_socket, client_address = server_socket.accept()
            print(f"📨 Новое подключение от {client_address}")
            
            try:
                # Получаем данные от клиента
                request_data = client_socket.recv(4096).decode('utf-8')
                
                if request_data:
                    print(f"📥 Получен запрос:\n{request_data.split(chr(13)+chr(10))[0]}")
                    
                    # Парсим HTTP запрос
                    method, path, body = parse_http_request(request_data)
                    
                    if method and path:
                        print(f"🔄 Обработка: {method} {path}")
                        
                        # Обрабатываем запрос в зависимости от метода
                        if method == "GET":
                            response = handle_get_request(path)
                        elif method == "POST":
                            response = handle_post_request(path, body)
                        else:
                            # Метод не поддерживается
                            response = handle_get_request("/404")
                        
                        # Отправляем ответ
                        client_socket.send(response)
                        print(f"✅ Ответ отправлен")
                    else:
                        print("❌ Не удалось распарсить запрос")
                
            except Exception as e:
                print(f"❌ Ошибка при обработке запроса: {e}")
            finally:
                # Закрываем соединение с клиентом
                client_socket.close()
                
    except KeyboardInterrupt:
        print("\n🛑 Сервер остановлен пользователем")
    except Exception as e:
        print(f"❌ Ошибка сервера: {e}")
    finally:
        server_socket.close()
        print("🔒 Socket закрыт")

if __name__ == "__main__":
    run_server()