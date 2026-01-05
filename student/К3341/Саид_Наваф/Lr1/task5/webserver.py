import socket
import json
from request import Request, Response
from lesson import Lessons, parse_get_grades_req, parse_set_grades_req, get_add_grade_form_html, parse_set_grades_form

HOST = "127.0.0.1"
PORT = 8081

class MyHTTPServer:
    def __init__(self, host, port, persist=None):  # Fixed: __init__ instead of init
        self.host = host
        self.port = port
        self.lessons = Lessons(persist)

    def serve_forever(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv:
            serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            serv.bind((self.host, self.port))
            serv.listen(5)
            print(f"HTTP server on http://{self.host}:{self.port}")
            while True:
                conn, _ = serv.accept()
                try:
                    self.serve_client(conn)
                except Exception as e:
                    print("Error handling client:", e)
                finally:
                    conn.close()

    def recv_line(self, conn):
        line = b""
        while not line.endswith(b"\r\n"):
            part = conn.recv(1)
            if not part:
                break
            line += part
        return line.decode()

    def parse_headers(self, conn):
        headers = {}
        while True:
            line = self.recv_line(conn)
            if not line or line == "\r\n":
                break
            name, value = line.split(":", 1)
            headers[name.strip().lower()] = value.strip()
        return headers

    def parse_request(self, conn) -> Request:
        # First line
        first_line = self.recv_line(conn)
        if not first_line:
            raise ConnectionError("No request line")
        method, url, version = first_line.strip().split(" ", 2)  # Fixed: use 2 instead of 3-1
        headers = self.parse_headers(conn)
        body = None
        if "content-length" in headers:
            length = int(headers["content-length"])
            body = conn.recv(length).decode()
        params = {}
        if "?" in url:
            path, query = url.split("?", 1)
            url = path
            for q in query.split("&"):
                if "=" in q:
                    k, v = q.split("=", 1)
                    params[k] = v
        return Request(method, url, version, params, headers, body)

    def send_response(self, conn, resp: Response):
        headers = resp.headers or {}
        if "Content-Length" not in headers:
            headers["Content-Length"] = str(len(resp.body.encode()))
        if "Content-Type" not in headers:
            headers["Content-Type"] = "text/html; charset=utf-8"
        header_lines = "".join(f"{k}: {v}\r\n" for k, v in headers.items())
        status_line = f"{resp.http_version} {resp.status} {resp.reason}\r\n"
        out = (status_line + header_lines + "\r\n" + resp.body).encode()
        conn.sendall(out)

    def handle_request(self, req: Request) -> Response:
        # Serve HTML form at root
        if req.method == "GET" and req.url == "/":
            return Response(200, "OK", body=get_add_grade_form_html())
        # View grades
        if req.method == "GET" and req.url == "/grades":
            return parse_get_grades_req(self.lessons, req)
        # Accept JSON POST to /grades (API)
        if req.method == "POST" and req.url == "/grades":
            return parse_set_grades_req(self.lessons, req)
        # Accept form POST from HTML form
        if req.method == "POST" and req.url == "/add":
            return parse_set_grades_form(self.lessons, req)
        return Response(404, "Not Found", body="Not Found")

    def serve_client(self, conn):
        req = self.parse_request(conn)
        resp = self.handle_request(req)
        self.send_response(conn, resp)

if __name__ == "__main__":
    s = MyHTTPServer(HOST, PORT, persist="grades.json")
    s.serve_forever()