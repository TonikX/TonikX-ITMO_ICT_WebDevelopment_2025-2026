import json
import socket
import sys
from email.parser import Parser
from functools import lru_cache
from urllib.parse import parse_qs, urlparse

MAX_LINE = 64 * 1024
MAX_HEADERS = 100


class MyHTTPServer:
    def __init__(self, host, port, server_name):
        self._host = host
        self._port = port
        self._server_name = server_name
        # Новая структура: {'Математика': [5, 4, 5], 'Физика': [3, 4]}
        self._grades = {}

    def serve_forever(self):
        serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            serv_sock.bind((self._host, self._port))
            serv_sock.listen()
            print(f"Сервер запущен: http://{self._host}:{self._port}/grades")
            while True:
                conn, _ = serv_sock.accept()
                try:
                    self.serve_client(conn)
                except Exception as e:
                    print('Ошибка при обработке клиента:', e)
        finally:
            serv_sock.close()

    def serve_client(self, conn):
        try:
            req = self.parse_request(conn)
            resp = self.handle_request(req)
            self.send_response(conn, resp)
        except ConnectionResetError:
            pass
        except Exception as e:
            self.send_error(conn, e)
        finally:
            if conn:
                try:
                    req.rfile.close()
                except:
                    pass
                conn.close()

    def parse_request(self, conn):
        rfile = conn.makefile('rb')
        method, target, ver = self.parse_request_line(rfile)
        headers = self.parse_headers(rfile)
        host = headers.get('Host')
        if not host:
            raise HTTPError(400, 'Bad Request', 'Заголовок Host обязателен')
        if host not in (self._server_name, f'{self._server_name}:{self._port}'):
            raise HTTPError(404, 'Not Found')
        return Request(method, target, ver, headers, rfile)

    def parse_request_line(self, rfile):
        raw = rfile.readline(MAX_LINE + 1)
        if len(raw) > MAX_LINE:
            raise HTTPError(400, 'Bad Request', 'Слишком длинная строка запроса')
        req_line = str(raw, 'iso-8859-1')
        words = req_line.rstrip('\r\n').split()
        if len(words) != 3:
            raise HTTPError(400, 'Bad Request', 'Некорректная строка запроса')
        method, target, ver = words
        if ver != 'HTTP/1.1':
            raise HTTPError(505, 'HTTP Version Not Supported')
        return method, target, ver

    def parse_headers(self, rfile):
        headers = []
        while True:
            line = rfile.readline(MAX_LINE + 1)
            if len(line) > MAX_LINE:
                raise HTTPError(494, 'Request header too large')
            if line in (b'\r\n', b'\n', b''):
                break
            headers.append(line)
            if len(headers) > MAX_HEADERS:
                raise HTTPError(494, 'Too many headers')
        sheaders = b''.join(headers).decode('iso-8859-1')
        return Parser().parsestr(sheaders)

    def handle_request(self, req):
        if req.path == '/grades' and req.method == 'POST':
            return self.handle_post_grade(req)
        if req.path == '/grades' and req.method == 'GET':
            return self.handle_get_grades(req)
        raise HTTPError(404, 'Not Found')

    def handle_post_grade(self, req):
        discipline = None
        grade = None

        # Сначала пробуем извлечь из ТЕЛА запроса (для HTML-формы)
        if req.method == 'POST':
            content_length_header = req.headers.get('Content-Length')
            if content_length_header:
                try:
                    content_length = int(content_length_header)
                    if content_length > 0:
                        body_data = req.body()
                        if body_data:
                            body_str = body_data.decode('utf-8')
                            parsed_body = parse_qs(body_str)
                            discipline = parsed_body.get(
                                'discipline', [None])[0]
                            grade = parsed_body.get('grade', [None])[0]
                except Exception as e:
                    print(f"Ошибка парсинга тела запроса: {e}")

        # Если в теле нет данных — пробуем СТРОКУ ЗАПРОСА (для curl)
        if discipline is None or grade is None:
            discipline = req.query.get('discipline', [None])[0]
            grade = req.query.get('grade', [None])[0]

        # Валидация
        if not discipline or not grade:
            raise HTTPError(400, 'Bad Request',
                            'Требуются параметры: discipline и grade')

        discipline_clean = discipline.strip()
        discipline_key = discipline_clean.lower()

        if not discipline_clean:
            raise HTTPError(400, 'Bad Request',
                            'Название дисциплины не может быть пустым')

        try:
            grade_int = int(grade)
            if not (1 <= grade_int <= 5):
                raise ValueError
        except ValueError:
            raise HTTPError(400, 'Bad Request',
                            'Оценка должна быть целым числом от 1 до 5')

        # Сохранение данных
        if discipline_key in self._grades:
            self._grades[discipline_key]['grades'].append(grade_int)
        else:
            self._grades[discipline_key] = {
                'name': discipline_clean,
                'grades': [grade_int]
            }

        return Response(204, 'Created')

    def handle_get_grades(self, req):
        accept = req.headers.get('Accept', '')

        if 'text/html' in accept:
            contentType = 'text/html; charset=utf-8'
            body = '<html><head><meta charset="utf-8"><title>Оценки</title></head><body>'
            body += '<h2>Список оценок по дисциплинам</h2>'

            if self._grades:
                body += '<ul>'
                # Сохраняем порядок добавления дисциплин (Python 3.7+)
                for data in self._grades.values():
                    discipline_name = data['name']
                    grades_list = data['grades']
                    # Форматируем оценки: "5, 4, 5 (среднее: 4.67)"
                    grades_str = ', '.join(str(g) for g in grades_list)
                    avg = sum(grades_list) / len(grades_list)
                    body += f'<li><strong>{discipline_name}:</strong> {grades_str} <em>(среднее: {avg:.2f})</em></li>'
                body += '</ul>'
            else:
                body += '<p>Нет записей.</p>'

            body += '''
            <hr>
            <h3>Добавить оценку</h3>
            <form method="POST" action="/grades">
                <label>Дисциплина: <input name="discipline" required></label><br><br>
                <label>Оценка (1-5): <input name="grade" type="number" min="1" max="5" required></label><br><br>
                <button type="submit">Добавить</button>
            </form>
            <hr>
            <a href="/grades">Обновить</a>
            </body></html>
            '''

        elif 'application/json' in accept:
            contentType = 'application/json; charset=utf-8'
            # Формируем удобочитаемый JSON: {"Математика": [5,4,5], ...}
            json_data = {data['name']: data['grades']
                         for data in self._grades.values()}
            body = json.dumps(json_data, ensure_ascii=False, indent=2)

        else:
            return Response(406, 'Not Acceptable')

        body = body.encode('utf-8')
        headers = [
            ('Content-Type', contentType),
            ('Content-Length', len(body))
        ]
        return Response(200, 'OK', headers, body)

    def send_response(self, conn, resp):
        wfile = conn.makefile('wb')
        status_line = f'HTTP/1.1 {resp.status} {resp.reason}\r\n'
        wfile.write(status_line.encode('iso-8859-1'))
        if resp.headers:
            for key, value in resp.headers:
                wfile.write(f'{key}: {value}\r\n'.encode('iso-8859-1'))
        wfile.write(b'\r\n')
        if resp.body:
            wfile.write(resp.body)
        wfile.flush()
        wfile.close()

    def send_error(self, conn, err):
        try:
            status = err.status
            reason = err.reason
            body = (err.body or reason).encode('utf-8')
        except:
            status = 500
            reason = 'Internal Server Error'
            body = b'Internal Server Error'
        headers = [('Content-Length', len(body))]
        resp = Response(status, reason, headers, body)
        self.send_response(conn, resp)


class Request:
    def __init__(self, method, target, version, headers, rfile):
        self.method = method
        self.target = target
        self.version = version
        self.headers = headers
        self.rfile = rfile



    @property
    def path(self):
        return self.url.path

    @property
    @lru_cache(maxsize=None)
    def query(self):
        return parse_qs(self.url.query)

    @property
    @lru_cache(maxsize=None)
    def url(self):
        return urlparse(self.target)

    def body(self):
        size = self.headers.get('Content-Length')
        if not size:
            return None
        return self.rfile.read(int(size))


class Response:
    def __init__(self, status, reason, headers=None, body=None):
        self.status = status
        self.reason = reason
        self.headers = headers or []
        self.body = body


class HTTPError(Exception):
    def __init__(self, status, reason, body=None):
        super()
        self.status = status
        self.reason = reason
        self.body = body


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Использование: python grade_server.py <host> <port> <server_name>")
        print("Пример: python grade_server.py localhost 8080 localhost")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    name = sys.argv[3]

    server = MyHTTPServer(host, port, name)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен.")
