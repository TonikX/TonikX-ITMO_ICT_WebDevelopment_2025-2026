import socket
import sys
from urllib.parse import urlparse, parse_qs

MAX_LINE = 64 * 1024

class GPAHTTPServer:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self.grades = {}

    def serve_forever(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self._host, self._port))
            s.listen(5)
            print(f"Server bind to http://{self._host}:{self._port}")
            while True:
                conn, addr = s.accept()
                with conn:
                    try:
                        self.serve_client(conn)
                    except Exception as e:
                        print("Error:", e)

    def serve_client(self, conn):
        rfile = conn.makefile("rb")
        method, path, version = self.parse_request(rfile)
        headers = self.parse_headers(rfile)
        body = b""
        if method == "POST":
            length = int(headers.get("Content-Length", 0))
            if length > 0:
                body = rfile.read(length)
        self.handle_request(conn, method, path, headers, body)

    def parse_request(self, rfile):
        line = rfile.readline(MAX_LINE + 1).decode("utf-8")
        if not line:
            raise Exception("Empty request")
        method, target, version = line.strip().split()
        return method, target, version

    def parse_headers(self, rfile):
        headers = {}
        while True:
            line = rfile.readline(MAX_LINE + 1).decode("utf-8")
            if line in ("\r\n", "\n", ""):
                break
            key, value = line.split(":", 1)
            headers[key.strip()] = value.strip()
        return headers

    def handle_request(self, conn, method, path, headers, body):
        parsed = urlparse(path)
        if method == "GET" and parsed.path == "/":
            content = self.render_page()
            self.send_response(conn, "200 OK", content)
        elif method == "POST" and parsed.path == "/":
            params = parse_qs(body.decode("utf-8"))
            subject = params.get("subject", [""])[0]
            grade = params.get("grade", [""])[0]
            if subject and grade:
                self.grades[subject] = self.grades.get(subject, []) + [grade]
            self.send_redirect(conn, "/")
        else:
            self.send_response(conn, "404 Not Found", "<h1>404 Not Found</h1>")

    def send_redirect(self, conn, location):
        headers = [
            "HTTP/1.1 303 See Other",
            f"Location: {location}",
            "Content-Length: 0",
            "Connection: close",
            "",
            "",
        ]
        response = "\r\n".join(headers).encode("utf-8")
        conn.sendall(response)


    def render_page(self):
        rows = "".join(
            f"<tr><td>{subject}</td><td>{', '.join(map(str, scores))}</td></tr>" for subject, scores in self.grades.items()
        )
        return f"""
        <html>
        <head><meta charset="utf-8"><title>Оценки</title></head>
        <body>
            <h1>Score Journal</h1>
            <table border="1" cellpadding="5" cellspacing="0">
                <tr><th>Subject</th><th>Score</th></tr>
                {rows}
            </table>
            <h2>Add Score</h2>
            <form method="POST" action="/">
                Subject: <input type="text" name="subject" required><br>
                Score: <input type="text" name="grade" required><br>
                <input type="submit" value="Add">
            </form>
        </body>
        </html>
        """

    def send_response(self, conn, status, body):
        body_bytes = body.encode("utf-8")
        headers = [
            f"HTTP/1.1 {status}",
            "Content-Type: text/html; charset=utf-8",
            f"Content-Length: {len(body_bytes)}",
            "Connection: close",
            "",
            "",
        ]
        response = "\r\n".join(headers).encode("utf-8") + body_bytes
        conn.sendall(response)

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8080
    serv = GPAHTTPServer(host, port)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        sys.exit()
