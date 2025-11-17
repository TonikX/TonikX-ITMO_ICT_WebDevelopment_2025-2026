import socket
from urllib.parse import unquote_plus

HOST = "localhost"
PORT = 12345

grades = {}

def handle_request(conn):
    """Обрабатывает HTTP запрос"""
    try:
        request_data = b""
        conn.settimeout(2.0)
        
        # Сначала читаем заголовки
        while b"\r\n\r\n" not in request_data:
            chunk = conn.recv(4096)
            if not chunk:
                break
            request_data += chunk
        
        # Если это POST запрос, читаем тело до конца
        if request_data.startswith(b"POST"):
            headers = request_data.split(b"\r\n\r\n")[0]
            content_length = 0
            for line in headers.split(b"\r\n"):
                if line.lower().startswith(b"content-length:"):
                    content_length = int(line.split(b":")[1].strip())
                    break
            
            body_start = request_data.find(b"\r\n\r\n") + 4
            current_body_length = len(request_data) - body_start
            
            while current_body_length < content_length:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                request_data += chunk
                current_body_length = len(request_data) - body_start
        
        request = request_data.decode('utf-8', errors='ignore')
        
        # Обрабатываем POST запрос
        post_success = False
        if request.startswith("POST") and "\r\n\r\n" in request:
            body = request.split("\r\n\r\n", 1)[1]
            parts = body.split("&")
            subject = ""
            grade = ""
            for part in parts:
                if part.startswith("subject="):
                    subject = unquote_plus(part[8:], encoding='utf-8')
                elif part.startswith("grade="):
                    grade = unquote_plus(part[6:], encoding='utf-8')
            
            # Добавляем оценку в список для данной дисциплины
            if subject and grade:
                if subject not in grades:
                    grades[subject] = []  # Создаем пустой список для новой дисциплины
                grades[subject].append(grade)  # Добавляем оценку в список
                post_success = True
                print(f"Добавлена оценка: {subject} - {grade}")
        
        # Генерируем HTML страницу
        rows = ""
        # Для каждой дисциплины отображаем все оценки через запятую
        for subject, grade_list in grades.items():
            grades_str = ", ".join(grade_list)  # Объединяем оценки в строку
            rows += f"<tr><td>{subject}</td><td>{grades_str}</td></tr>"
        
        success_msg = ""
        if post_success:
            success_msg = '<p style="color: green; font-weight: bold;">Оценка успешно добавлена!</p>'
        
        html_content = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Оценки по дисциплинам</title>
            </head>
            <body>
                <h1>Добавить оценку</h1>
                <form method="POST">
                    Дисциплина: <input type="text" name="subject" required><br>
                    Оценка: <input type="text" name="grade" required><br>
                    <input type="submit" value="Добавить">
                </form>
                
                {success_msg}
                
                <h2>Все оценки</h2>
                <table border="1">
                    <tr><th>Дисциплина</th><th>Оценки</th></tr>
                    {rows}
                </table>
            </body>
            </html>"""
        
        # Формируем HTTP ответ
        response = f"HTTP/1.1 200 OK\r\n"
        response += "Content-Type: text/html; charset=utf-8\r\n"
        response += f"Content-Length: {len(html_content.encode('utf-8'))}\r\n"
        response += "\r\n"
        response += html_content
        
        conn.sendall(response.encode('utf-8'))
        print("Ответ успешно отправлен")
        
    except socket.timeout:
        print("Таймаут при чтении запроса")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        conn.close()

def main():
    """Запускает сервер"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(5)
        
        print(f"Сервер запущен на http://{HOST}:{PORT}")
        
        try:
            while True:
                conn, addr = server.accept()
                print(f"Новое подключение от {addr[0]}:{addr[1]}")
                handle_request(conn)
        except KeyboardInterrupt:
            print("\nСервер остановлен")

if __name__ == "__main__":
    main()