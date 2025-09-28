import socket
import threading
import urllib.parse
import json
import os
import html
from datetime import datetime, timezone

HOST = '127.0.0.1'
PORT = 8005
ENCODING = 'utf-8'
DATA_FILE = 'grades.json'
LOCK = threading.Lock()
SERVER_NAME = 'SimpleGradesServer/1.0'

def load_data():
    """Загружает данные из JSON файла"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_data(data):
    """Сохраняет данные в JSON файл"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def render_page(data):
    """Создает HTML страницу с таблицей оценок"""
    subjects = {}
    for item in data:
        subject = item['subject']
        grade = item['grade']
        if subject not in subjects:
            subjects[subject] = []
        subjects[subject].append(grade)

    if subjects:
        rows = ""
        for subject, grades in subjects.items():
            grades_str = ", ".join(grades)
            rows += f"<tr><td>{html.escape(subject)}</td><td>{html.escape(grades_str)}</td></tr>\n"
    else:
        rows = '<tr><td colspan="2" style="text-align: center; color: #999;">Пока нет оценок</td></tr>\n'

    total_grades = len(data)
    avg_grade = sum(int(item['grade']) for item in data if item['grade'].isdigit()) / total_grades if total_grades > 0 else 0

    with open('template.html', 'r', encoding='utf-8') as f:
        template = f.read()

    # Заменяем плейсхолдеры вручную, чтобы избежать конфликтов с CSS
    html_content = template.replace('{total_grades}', str(total_grades))
    html_content = html_content.replace('{avg_grade:.1f}', f'{avg_grade:.1f}')
    html_content = html_content.replace('{rows}', rows)
    
    return html_content.encode(ENCODING)

def create_http_response(status_code, body, content_type='text/html; charset=utf-8'):
    """Создает HTTP ответ с заданным статус-кодом и телом"""
    status_text = {
        200: "200 OK",
        303: "303 See Other",
        404: "404 Not Found",
        405: "405 Method Not Allowed"
    }.get(status_code, "500 Internal Server Error")
    
    headers = [
        f"HTTP/1.1 {status_text}",
        f"Server: {SERVER_NAME}",
        f"Content-Type: {content_type}",
        f"Content-Length: {len(body)}",
        f"Date: {datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')}",
        "Connection: close",
        "",
        ""
    ]
    return "\r\n".join(headers).encode(ENCODING) + body

def http_redirect(location):
    """Создает HTTP редирект"""
    headers = [
        "HTTP/1.1 303 See Other",
        f"Location: {location}",
        f"Server: {SERVER_NAME}",
        f"Date: {datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')}",
        "Connection: close",
        "",
        ""
    ]
    return "\r\n".join(headers).encode(ENCODING)

def handle_client(conn, addr):
    """Обрабатывает HTTP запрос от клиента"""
    with conn:
        try:
            req = conn.recv(8192).decode(ENCODING)
            if not req:
                return

            lines = req.splitlines()
            if not lines:
                return
                
            first_line = lines[0]
            parts = first_line.split()
            if len(parts) < 3:
                return
                
            method, path, version = parts
            headers_body = req.split("\r\n\r\n", 1)
            headers = headers_body[0]
            body = headers_body[1] if len(headers_body) > 1 else ""
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {addr} -> {method} {path}")

            if method == 'GET' and path == '/':
                with LOCK:
                    data = load_data()
                response = create_http_response(200, render_page(data))
                conn.sendall(response)

            elif method == 'POST' and path == '/add':
                content_type_line = next((line for line in headers.splitlines() if line.lower().startswith('content-type:')), "")
                
                if 'application/x-www-form-urlencoded' in content_type_line:
                    parsed = urllib.parse.parse_qs(body)
                    subject = urllib.parse.unquote(parsed.get('subject', [''])[0]).strip()
                    grade = urllib.parse.unquote(parsed.get('grade', [''])[0]).strip()
                    
                    # Валидация данных
                    if subject and grade and grade.isdigit() and 1 <= int(grade) <= 5:
                        with LOCK:
                            data = load_data()
                            data.append({"subject": subject, "grade": grade})
                            save_data(data)
                        print(f"Добавлена оценка: {subject} - {grade}")
                        conn.sendall(http_redirect('/'))
                    else:
                        error_html = "<html><body><h1>Ошибка валидации</h1><p>Проверьте правильность введенных данных.</p><a href='/'>Вернуться на главную</a></body></html>"
                        response = create_http_response(400, error_html.encode(ENCODING))
                        conn.sendall(response)
                else:
                    error_html = "<html><body><h1>Ошибка</h1><p>Неподдерживаемый Content-Type</p><a href='/'>Вернуться на главную</a></body></html>"
                    response = create_http_response(415, error_html.encode(ENCODING))
                    conn.sendall(response)
            else:
                error_html = """
                <!DOCTYPE html>
                <html><head><title>404 Not Found</title></head>
                <body><h1>404 Not Found</h1>
                <p>Страница не найдена</p>
                <p><a href="/">Вернуться на главную</a></p>
                </body></html>
                """
                response = create_http_response(404, error_html.encode(ENCODING))
                conn.sendall(response)
                
        except Exception as e:
            print(f"Ошибка обработки запроса от {addr}: {e}")

def main():
    print("HTTP Сервер")
    print("=" * 20)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        
        print(f"Сервер запущен на http://{HOST}:{PORT}/")
        print(f"Файл: template.html")
        print(f"Протокол: HTTP/1.1")
        print(f"Многопоточность: Включена")
        print("\nНажмите Ctrl+C для остановки...")
        
        try:
            while True:
                conn, addr = s.accept()
                thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
                thread.start()
        except KeyboardInterrupt:
            print("\nСервер остановлен")

if __name__ == '__main__':
    main()
