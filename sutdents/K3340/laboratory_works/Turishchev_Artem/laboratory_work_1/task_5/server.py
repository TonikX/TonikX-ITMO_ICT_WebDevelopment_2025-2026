import socket
from config import HOST, PORT

class MyHTTPServer:
    def __init__(self, host, port, name):
        self.host = host
        self.port = port
        self.name = name
        self.grades = dict()

    def serve_forever(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen(10)
        print(f"Сервер запущен на http://{self.host}:{self.port}")

        try:
            while True:
                client_sock, _ = sock.accept()
                self.serve_client(client_sock)
        finally:
            sock.close()

    def serve_client(self, client_sock):
        try:
            client_file = client_sock.makefile('rb')
            method, url, version, params = self.parse_request(client_file, client_sock)
            headers = self.parse_headers(client_file)
            self.handle_request(client_sock, method, params)
            client_file.close()
        except Exception as e:
            print(e)
            self.send_error(client_sock, "400 Bad Request")
        finally:
            client_sock.close()

    def parse_request(self, client_file, client_sock):
        request_line = client_file.readline().decode().strip()
        if not request_line:
            raise ValueError("Пустая строка запроса")
        parts = request_line.split()
        if len(parts) != 3:
            raise ValueError("Неверный формат строки запроса")
        method, url, version = parts
        params = dict()
        if '?' in url:
            try:
                url, params = url.split("?")
                tmp = params.split("&")
                params = dict()
                for i in tmp:
                    key, value = i.split("=")
                    params[key] = value
            except Exception as e:
                print(e)
                self.send_error(client_sock, "400 Bad Request")
        return method, url, version, params

    def parse_headers(self, client_file):
        headers = {}
        while True:
            line = client_file.readline().decode().strip()
            if line == '':
                break
            key, value = line.split(':', 1)
            headers[key.strip()] = value.strip()
        return headers

    def handle_request(self, client_sock, method, params):
        if method == 'GET':
            html = "<html><head><meta charset='utf-8'><title>Оценки</title></head><body>"
            html += "<h1>Оценки по дисциплинам</h1>"
            if self.grades:
                html += "<ul>"
                for disc, grade in self.grades.items():
                    html += f"<li>{disc}: {", ".join(grade)}</li>"
                html += "</ul>"
            else:
                html += "<p>Нет сохранённых оценок.</p>"
            self.send_response(client_sock, "200 OK", "text/html; charset=utf-8", html)
        elif method == 'POST':
            for key in params:
                if key in self.grades:
                    self.grades[key].append(params[key])
                else:
                    self.grades[key] = [params[key]]
            self.send_response(client_sock, "200 OK", "text/plain; charset=utf-8", "OK")
        else:
            self.send_error(client_sock, "404 Not Found")

    def send_error(self, client_sock, status):
        self.send_response(client_sock, status, "text/html; charset=utf-8", f"<h1>{status}</h1>")

    def send_response(self, client_sock, status, content_type, body):
        response = f"HTTP/1.1 {status}\r\n"
        response += f"Server: {self.name}\r\n"
        response += f"Connection: close\r\n"
        response += f"Content-Type: {content_type}\r\n"
        response += f"Content-Length: {len(body.encode())}\r\n"
        response += "\r\n"
        response += body
        client_sock.send(response.encode())

if __name__ == '__main__':
    host = HOST
    port = PORT
    name = "Grades"
    serv = MyHTTPServer(host, port, name)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        pass