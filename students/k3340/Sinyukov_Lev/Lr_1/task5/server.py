import socket
# import sys
from urllib.parse import parse_qs, unquote, urlparse


class MyHTTPServer:
    def __init__(self, host, port, server_name):
        self.host = host
        self.port = port
        self.server_name = server_name
        self.grades = {}  # Словарь для хранения оценок

    def serve_forever(self):
        # Запуск сервера на сокете, обработка входящих соединений
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)

        print(f"Сервер {self.server_name} запущен на {self.host}:{self.port}")

        try:
            while True:
                client_socket, addr = server_socket.accept()
                print(f"Подключен клиент: {addr}")
                self.serve_client(client_socket)
        except KeyboardInterrupt:
            print("\nСервер остановлен")
        finally:
            server_socket.close()

    def serve_client(self, client_socket):
        # Обработка подключения
        try:
            # Создаем объект из сокета для построчного чтения
            client_file = client_socket.makefile('rwb', buffering=0)

            # Парсим HTTP запрос
            method, url, params, headers, body = self.parse_request(client_file)

            # Обрабатываем запрос
            response, status_code = self.handle_request(method, url, params, headers, body)

            # Отправляем ответ
            self.send_response(client_socket, response, status_code)

        except Exception as e:
            print(f"Ошибка при обработке клиента: {e}")
            # В случае ошибки отправляем 500 Internal Server Error
            error_html = "<html><body><h1>500 Internal Server Error</h1></body></html>"
            self.send_response(client_socket, error_html, 500)
        finally:
            client_socket.close()

    def parse_request(self, client_file):
        # Обработка заголовка HTTP запроса
        request_line = client_file.readline().decode('utf-8').strip()
        if not request_line:
            raise ValueError("Пустой запрос")

        # Разбиваем на метод, URL и версию протокола
        method, url, version = request_line.split()
        print(f"Запрос: {method} {url} {version}")

        # Парсим URL и параметры
        parsed_url = urlparse(url)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)

        # Обработка headers
        headers = {}
        while True:
            header_line = client_file.readline().decode('utf-8').strip()
            if not header_line:  # Пустая строка - конец заголовка
                break
            if ':' in header_line:
                key, value = header_line.split(':', 1)
                headers[key.strip()] = value.strip()

        # Читаем тело запроса для POST
        body = ""
        if method == 'POST' and 'Content-Length' in headers:
            content_length = int(headers['Content-Length'])
            body = client_file.read(content_length).decode('utf-8')

        return method, path, query_params, headers, body

    def handle_request(self, method, url, params, headers, body):
        # Обработка url в соответствии с нужным методом
        if url == '/' or url == '/grades':
            if method == 'GET':
                return self.handle_get_grades(), 200
            elif method == 'POST':
                return self.handle_post_grade(body), 200
            else:
                return self.build_error_html("Method Not Allowed"), 405
        else:
            return self.build_error_html("Not Found"), 404

    def handle_get_grades(self):
        # Обработка GET запроса - возвращаем HTML с оценками
        html = self.build_html()
        return html

    def handle_post_grade(self, body):
        # Обработка POST запроса - добавляем новую оценку
        parsed_body = parse_qs(body)
        discipline = unquote(parsed_body.get('discipline', [''])[0])
        grade_str = parsed_body.get('grade', [''])[0]

        if discipline and grade_str:
            try:
                grade = int(grade_str)
                if 2 <= grade <= 5:
                    self.grades.setdefault(discipline, []).append(grade)
                    print(f"Добавлена оценка: {discipline} - {grade}")
            except ValueError:
                pass  # Некорректная оценка

        # После POST возвращаем ту же страницу с обновленными данными
        return self.build_html()

    def build_html(self):
        # Генерация HTML страницы
        html = """
            <!DOCTYPE html>
            <html lang="ru">
            <head>
                <meta charset="UTF-8">
                <title>Журнал оценок</title>
                <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&display=swap" rel="stylesheet">
                <style>
                    body {
                        font-family: 'Roboto', sans-serif;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        margin: 0;
                        padding: 0;
                        min-height: 100vh;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                    }
                    .container {
                        background: white;
                        padding: 40px;
                        border-radius: 15px;
                        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                        max-width: 600px;
                        width: 90%;
                        text-align: center;
                    }
                    h1 {
                        color: #333;
                        margin-bottom: 30px;
                        font-weight: 500;
                        font-size: 2.5em;
                    }
                    h2 {
                        color: #555;
                        margin-top: 30px;
                        margin-bottom: 20px;
                        font-weight: 400;
                    }
                    form {
                        background: #f8f9fa;
                        padding: 25px;
                        border-radius: 10px;
                        margin-bottom: 20px;
                    }
                    label {
                        display: block;
                        margin-bottom: 15px;
                        font-weight: 500;
                        color: #333;
                        text-align: left;
                    }
                    input {
                        width: 100%;
                        padding: 12px;
                        margin-top: 5px;
                        border: 2px solid #ddd;
                        border-radius: 8px;
                        font-size: 16px;
                        box-sizing: border-box;
                        transition: border-color 0.3s;
                    }
                    input:focus {
                        outline: none;
                        border-color: #667eea;
                    }
                    button {
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        border: none;
                        padding: 15px 30px;
                        border-radius: 8px;
                        font-size: 16px;
                        cursor: pointer;
                        transition: transform 0.2s;
                        font-weight: 500;
                    }
                    button:hover {
                        transform: translateY(-2px);
                    }
                    hr {
                        border: none;
                        height: 2px;
                        background: linear-gradient(90deg, transparent, #667eea, transparent);
                        margin: 30px 0;
                    }
                    .grade-item {
                        background: #f8f9fa;
                        margin: 15px 0;
                        padding: 15px;
                        border-radius: 8px;
                        border-left: 4px solid #667eea;
                        text-align: left;
                    }
                    .no-grades {
                        color: #666;
                        font-style: italic;
                        margin: 30px 0;
                    }
                    .subject-name {
                        color: #333;
                        font-weight: 500;
                        margin-bottom: 5px;
                    }
                    .grades-list {
                        color: #666;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>📚 Журнал оценок</h1>
                    <form method="POST" action="/">
                        <label>Дисциплина:
                            <input name="discipline" placeholder="Введите название дисциплины" required>
                        </label>
                        <label>Оценка:
                            <input name="grade" type="number" min="2" max="5" placeholder="Введите оценку от 2 до 5" required>
                        </label>
                        <button type="submit">📝 Добавить оценку</button>
                    </form>
                    <hr>
                    <h2>Список оценок</h2>
            """

        if self.grades:
            for subject, marks in self.grades.items():
                html += f'<div class="grade-item"><b>{subject}</b>: {", ".join(map(str, marks))}</div>'
        else:
            html += '<p>Пока нет оценок</p>'

        html += """
    </div>
</body>
</html>"""
        return html

    def build_error_html(self, message):
        # Генерация HTML страницы ошибки
        return f"""<!DOCTYPE html>
<html>
<head><title>Error</title></head>
<body>
    <h1>{message}</h1>
    <a href="/">Вернуться на главную</a>
</body>
</html>"""

    def send_response(self, client_socket, response, status_code=200):
        # Отправка ответа
        status_messages = {
            200: 'OK',
            404: 'Not Found',
            405: 'Method Not Allowed',
            500: 'Internal Server Error'
        }

        status_line = f"HTTP/1.1 {status_code} {status_messages.get(status_code, 'Unknown')}\r\n"
        headers = [
            "Content-Type: text/html; charset=utf-8",
            f"Content-Length: {len(response.encode('utf-8'))}",
            "Connection: close",
            ""
        ]

        response_data = status_line + "\r\n".join(headers) + "\r\n" + response
        client_socket.sendall(response_data.encode('utf-8'))


if __name__ == '__main__':
    host = 'localhost'
    port = 8080
    name = 'EvaluationSheet'

    serv = MyHTTPServer(host, port, name)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        pass