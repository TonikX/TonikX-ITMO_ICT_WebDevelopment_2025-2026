import socket
from urllib.parse import parse_qs
from email.parser import Parser
from students.k3341.Smirnova_Karina.Lab1.task5.Request import Request
from students.k3341.Smirnova_Karina.Lab1.task5.Response import Response

MAX_LINE = 64*1024
MAX_HEADERS = 100

# GET /marks
# POST /addMark?sub=Biology&mark=4

class MyHttpServer:
    def __init__(self, host, port, server_name):
        self.host = host
        self.port = port
        self.server_name = server_name
        self.marks = {}

    def serve_forever(self):
        """Запуск сервера на сокете, обработка входящих соединений"""

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            server_socket.bind((self.host, self.port))
            server_socket.listen()

            while True:
                client_socket, address = server_socket.accept()

                try:
                    self.serve_client(client_socket)

                except Exception as e:
                    print("Client serving failed: ", e)
        finally:
            server_socket.close()

    def serve_client(self, client_socket):
        """Обработка клиентского подключения"""

        try:
            request = self.parse_request(client_socket)
            response = self.handle_request(request)
            self.send_response(client_socket, response)

        except ConnectionResetError:
            client_socket = None
        except Exception as e:
            print('Error: ', e)
            self.send_error(client_socket, e)

        if client_socket:
            client_socket.close()

    def parse_request(self, client_socket):
        """Функция для обработки заголовка http запроса"""

        rfile = client_socket.makefile('rb')  # Обернули сокет в бинарный файл
        method, target, ver = self.parce_request_line(rfile)
        headers = self.parce_headers(rfile)

        host = headers.get('Host')
        if not host:
            raise Exception('Bad request')

        if host not in (self.host, f'{self.host}:{self.port}', self.server_name, f'{self.server_name}:{self.port}'):
            raise Exception('Not found host')

        request = Request(method, target, ver, headers, rfile)
        if method == 'POST':
            form_fields = self.parse_post_form(request)
            request.form = form_fields

        return request

    def parce_request_line(self, rfile):
        """Обработка строки запроса"""

        raw = rfile.readline(MAX_LINE + 1)
        if len(raw) > MAX_LINE:
            raise Exception("Request line is too long")

        request_line = str(raw, 'iso-8859-1')
        request_line = request_line.strip('\r\n')
        words = request_line.split()
        if len(words) != 3:
            raise Exception('Wrong request format')

        method, target, ver = words
        if ver != 'HTTP/1.1':
            raise Exception("Unexpected HTTP version")

        return method, target, ver

    def parce_headers(self, rfile):
        """Обработка заголовков запроса"""

        headers = []

        while True:
            line = rfile.readline(MAX_LINE + 1)
            if len(line) > MAX_LINE:
                raise Exception('Header line is to loong')

            # Конец заголовков
            if line in (b'\r\n', b'\n', b''):
                break

            headers.append(line)

            if len(headers) > MAX_HEADERS:
                raise Exception('Too many headers')

        headers_dict = b''.join(headers).decode('iso-8859-1')

        return Parser().parsestr(headers_dict)

    def parse_post_form(self, request):
        """Достаем параметры из формы"""

        content_length = int(request.headers.get('Content-Length', 0))
        if content_length > 0:
            body = request.rfile.read(content_length).decode('utf-8')
            return parse_qs(body)
        return {}

    def handle_request(self, request):
        """Обработка запроса"""

        if request.path == '/marks' and request.method == 'GET':
            return self.handle_get_marks(request)

        elif request.path == '/addMark' and request.method == 'POST':
            return self.handle_post_addMark(request)

        else:
            raise Exception(f'Unknown path {request.path} or method {request.method}')

    def handle_get_marks(self, request):
        """Получение оценок"""

        accept = request.headers.get('Accept')
        if 'text/html' in accept:
            contentType = 'text/html; charset=utf-8'
            body = '<html><head></head><body>'
            body += f'<div>Оценки ({len(self.marks)})</div>'
            body += '<ul>'
            for sub, marks in self.marks.items():
                marks_str = ', '.join(str(m) for m in marks)
                body += f'<li>{sub}: {marks_str}</li>'
            body += '</ul>'

            # Форма для добавления оценки
            body += '''
                    <h3>Добавить оценку</h3>
                    <form action="/addMark" method="POST">
                        <label>Предмет: <input type="text" name="sub" required></label><br>
                        <label>Оценка: <input type="number" name="mark" step="any" required></label><br>
                        <button type="submit">Добавить</button>
                    </form>
                    '''

            body += '</body></html>'

        else:
            return Response(406, 'Not Acceptable')

        body = body.encode('utf-8')
        headers = [('Content-Type', contentType),
                   ('Content-Length', len(body))]

        return Response(200, 'OK', headers, body)

    def handle_post_addMark(self, request):
        """Добавление предмета и оценки в список"""

        subject = request.form['sub'][0]
        mark = float(request.form['mark'][0])
        if subject not in self.marks:
            self.marks[subject] = []
        self.marks[subject].append(mark)

        headers = [('Location', '/marks')]
        return Response(303, 'Redirect', headers)

    def send_response(self, client_socket, response):
        """Формирование HTTP ответа"""

        wfile = client_socket.makefile('wb')
        status_line = f'HTTP/1.1 {response.status} {response.reason}\r\n'
        wfile.write(status_line.encode('iso-8859-1'))

        if response.headers:
            for key, val in response.headers:
                header_line = f'{key}: {val}\r\n'
                wfile.write(header_line.encode('iso-8859-1'))

        wfile.write(b'\r\n')

        if response.body:
            wfile.write(response.body)

        wfile.flush()
        wfile.close()

    def send_error(self, client_socket, err):
        """Формирование страницы ошибки"""

        try:
            status = err.status
            reason = err.reason
            body = (err.body or err.reason).encode('utf-8')
        except:
            status = 500
            reason = b'Internal Server Error'
            body = b'Internal Server Error'

        resp = Response(status, reason,
                        [('Content-Length', len(body))],
                        body)
        self.send_response(client_socket, resp)

if __name__ == "__main__":
    host = 'localhost'
    port = 8080
    name = 'serverName.com'

    server = MyHttpServer(host, port, name)
    try:
        server.serve_forever()
        print("Server is ready for work")
    except KeyboardInterrupt:
        pass