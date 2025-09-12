import socket
import sys
from urllib.parse import parse_qs, urlparse


class MyHTTPServer:
    # Параметры сервера

    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.grades = {}  # Хранилище для оценок: {'Дисциплина': [Оценка1, Оценка2]}

    def serve_forever(self):
        """1. Запуск сервера на сокете, обработка входящих соединений"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # try:
        server_socket.bind((self.host, self.port))
        server_socket.listen(1)
        print(f'Сервер запущен на http://{self.host}:{self.port}')

        while True:
            # Ожидаем клиентское подключение
            connection, client_address = server_socket.accept()
            print(f"Подключен клиент: {client_address}")
            # try:
            self.serve_client(connection)
            # except Exception as e:
            #     print(f"Ошибка при обработке клиента: {e}")
            # finally:
            connection.close()
        # finally:
        server_socket.close()

    def serve_client(self, connection):
        """2. Обработка клиентского подключения"""
        # Используем makefile для удобного чтения данных из сокета
        rfile = connection.makefile('rb')

        # 3. Парсим первую строку запроса (метод, URL, версия)
        method, path, version = self.parse_request(rfile)

        # 4. Парсим заголовки
        headers = self.parse_headers(rfile)

        # Читаем тело запроса, если оно есть (для POST)
        body = b''
        if 'Content-Length' in headers:
            try:
                content_length = int(headers['Content-Length'])
                body = rfile.read(content_length)
            except (ValueError, TypeError):
                print("Неверное значение Content-Length")

        # 5. Обрабатываем запрос и получаем компоненты ответа
        response_code, response_reason, response_headers, response_body = self.handle_request(method, path, body)

        # 6. Отправляем ответ клиенту
        self.send_response(connection, response_code, response_reason, response_headers, response_body)

    def parse_request(self, rfile):
        """3. функция для обработки заголовка http+запроса.
        Python, сокет предоставляет возможность создать вокруг него некоторую обертку,
        которая предоставляет file object интерфейс. Это дайте возможность построчно обработать запрос.
        Заголовок всегда - первая строка.
        Первую строку нужно разбить на 3 элемента (метод + url + версия протокола).
        URL необходимо разбить на адрес и параметры (isu.ifmo.ru/pls/apex/f?p=2143,
        где isu.ifmo.ru/pls/apex/f, а p=2143 - параметр p со значением 2143)"""
        raw = rfile.readline()

        request_line = str(raw, 'iso-8859-1').rstrip('\r\n')
        words = request_line.split()
        if len(words) != 3:
            raise Exception('Неверный формат строки запроса')

        method, target, version = words
        return method, target, version

    def parse_headers(self, rfile):
        """4. Функция для обработки headers.
        Необходимо прочитать все заголовки после первой строки до появления пустой строки
        и сохранить их в массив."""
        headers = {}
        while True:
            line = rfile.readline(65537)
            if line in (b'\r\n', b'\n', b''):
                break

            line_str = str(line, 'iso-8859-1').rstrip('\r\n')
            key, value = line_str.split(':', 1)
            headers[key.strip()] = value.strip()

        return headers

    def handle_request(self, method, path, body):
        """5. Функция для обработки url в соответствии с нужным методом.
        В случае данной работы, нужно будет создать набор условий,
        который обрабатывает GET или POST запрос. GET запрос должен возвращать данные.
        POST запрос должен записывать данные на основе переданных параметров."""
        # GET-запрос на главную страницу
        if method == 'GET' and path == '/':
            html_content = self._generate_html_page()
            body_bytes = html_content.encode('utf-8')
            headers = {
                'Content-Type': 'text/html; charset=utf-8',
                'Content-Length': str(len(body_bytes))
            }
            return 200, 'OK', headers, body_bytes

        # POST-запрос на добавление оценки
        elif method == 'POST' and path == '/add_grade':
            # Парсим тело POST-запроса
            data_str = body.decode('utf-8')
            parsed_data = parse_qs(data_str)

            subject = parsed_data.get('subject', [''])[0]
            grade = parsed_data.get('grade', [''])[0]

            if subject and grade:
                self.grades[subject] = self.grades.get(subject, []) + [grade]
                print(f"Обновлены оценки: {self.grades}")

            # Делаем редирект на главную страницу
            headers = {'Location': '/'}
            return 303, 'See Other', headers, b''

        # Если страница не найдена
        else:
            body_bytes = b"404 Not Found"
            headers = {
                'Content-Type': 'text/plain',
                'Content-Length': str(len(body_bytes))
            }
            return 404, 'Not Found', headers, body_bytes

    def send_response(self, connection, code, reason, headers, body):
        """6. Функция для отправки ответа. Необходимо записать в соединение
        status line вида HTTP/1.1 <status_code> <reason>.
        Затем, построчно записать заголовки и пустую строку, обозначающую конец секции заголовков."""
        # Формируем статус-строку
        status_line = f"HTTP/1.1 {code} {reason}\r\n"
        connection.sendall(status_line.encode('iso-8859-1'))

        # Отправляем заголовки
        for key, value in headers.items():
            header_line = f"{key}: {value}\r\n"
            connection.sendall(header_line.encode('iso-8859-1'))

        # Пустая строка после заголовков
        connection.sendall(b'\r\n')

        # Отправляем тело ответа, если оно есть
        if body:
            connection.sendall(body)

    def _generate_html_page(self):
        """Вспомогательная функция для генерации HTML-страницы."""
        body = "<h1>Оценки по дисциплинам</h1>"

        if self.grades:
            body += "<ul>"
            for subject, grade in self.grades.items():
                body += f"<li>{subject}: {grade}</li>"
            body += "</ul>"
        else:
            body += "<p>Оценок пока нет.</p>"

        body += """
            <h2>Добавить оценку</h2>
            <form method="post" action="/add_grade">
                <label for="subject">Дисциплина:</label><br>
                <input type="text" id="subject" name="subject" required><br>
                <label for="grade">Оценка:</label><br>
                <input type="text" id="grade" name="grade" required><br><br>
                <input type="submit" value="Добавить">
            </form>
        """
        return f"<html><head><title>Система оценок</title><meta charset='utf-8'></head><body>{body}</body></html>"
