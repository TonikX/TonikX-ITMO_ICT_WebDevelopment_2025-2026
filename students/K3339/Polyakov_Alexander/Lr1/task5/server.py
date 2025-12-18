# server.py
import socket
import sys
from urllib.parse import urlsplit, parse_qs
from email.utils import formatdate

HOST = "127.0.0.1"
PORT = 8080
NAME = "SERVER"

MAX_LINE = 64 * 1024
MAX_HEADERS = 100

GRADES: dict[str, list[str]] = {}  # subject -> list of grades

class HTTPError(Exception):
    def __init__(self, status: int, reason: str, body: str | None = None):
        super().__init__(reason)
        self.status = status
        self.reason = reason
        self.body = body or reason


class Request:
    """A minimal request envelope similar to the guide."""
    def __init__(self, method: str, target: str, version: str, rfile):
        self.method = method
        self.target = target
        self.version = version
        self.rfile = rfile
        self.headers: dict[str, str] = {}
        # Derived:
        parts = urlsplit(target)
        self.path = parts.path or "/"
        self.query = parse_qs(parts.query, keep_blank_values=True)

    def body(self) -> bytes | None:
        """Read request body using Content-Length (per guide’s approach)."""
        size = self.headers.get("content-length")
        if not size:
            return None
        try:
            n = int(size)
        except ValueError:
            raise HTTPError(400, "Bad Request", "Invalid Content-Length")
        if n < 0:
            raise HTTPError(400, "Bad Request", "Negative Content-Length")
        return self.rfile.read(n)


class Response:
    def __init__(self,
                 status: int,
                 reason: str,
                 headers: list[tuple[str, str]] | None = None,
                 body: bytes | None = None):
        self.status = status
        self.reason = reason
        self.headers = headers or []
        self.body = body


class MyHTTPServer:
    def __init__(self, host: str, port: int, server_name: str):
        self._host = host
        self._port = port
        self._server_name = server_name

    def serve_forever(self):
        # 1. Запуск сервера на сокете, обработка входящих соединений
        serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
        serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serv_sock.bind((self._host, self._port))
        serv_sock.listen(50)
        print(f"HTTP server '{self._server_name}' is listening on http://{self._host}:{self._port}")

        try:
            while True:
                conn, addr = serv_sock.accept()
                try:
                    self.serve_client(conn, addr)
                except Exception as e:
                    # best-effort error reporting
                    try:
                        self.send_error(conn, e)
                    except Exception:
                        pass
                finally:
                    try:
                        conn.close()
                    except OSError:
                        pass
        finally:
            serv_sock.close()

    def serve_client(self, conn: socket.socket, addr):
        # 2. Обработка клиентского подключения
        req = self.parse_request(conn)
        resp = self.handle_request(req)
        self.send_response(conn, resp)

    def parse_request(self, conn: socket.socket) -> Request:
        # 3. Разбор request line (метод + url + версия) и подготовка rfile

        # file-like
        rfile = conn.makefile("rb")
        req_line = rfile.readline(MAX_LINE + 1)
        if len(req_line) > MAX_LINE:
            raise HTTPError(414, "Request-URI Too Long")
        if not req_line:
            raise HTTPError(400, "Bad Request", "Empty request line")

        # HTTP uses ISO-8859-1 for headers/line-level bytes
        try:
            req_line_str = req_line.decode("iso-8859-1").rstrip("\r\n")
        except UnicodeDecodeError:
            raise HTTPError(400, "Bad Request", "Invalid request line encoding")

        parts = req_line_str.split()
        if len(parts) != 3:
            raise HTTPError(400, "Bad Request", "Malformed request line")

        method, target, version = parts
        if version != "HTTP/1.1":
            raise HTTPError(505, "HTTP Version Not Supported")

        req = Request(method, target, version, rfile)
        req.headers = self.parse_headers(rfile)

        if "host" not in req.headers:
            raise HTTPError(400, "Bad Request", "Host header is missing")

        return req

    def parse_headers(self, rfile) -> dict[str, str]:
        # 4. Функция для обработки headers до пустой строки
        headers: dict[str, str] = {}
        for _ in range(MAX_HEADERS):
            line = rfile.readline(MAX_LINE + 1)
            if len(line) > MAX_LINE:
                raise HTTPError(494, "Request header too large")
            if line in (b"\r\n", b"\n", b""):
                break
            try:
                line_str = line.decode("iso-8859-1").rstrip("\r\n")
            except UnicodeDecodeError:
                raise HTTPError(400, "Bad Request", "Invalid header encoding")
            if ":" not in line_str:
                continue
            name, value = line_str.split(":", 1)
            headers[name.strip().lower()] = value.strip()
        else:
            raise HTTPError(400, "Bad Request", "Too many headers")
        return headers

    def handle_request(self, req: Request) -> Response:
        # 5. Роутинг и обработка GET/POST
        if req.method == "GET" and req.path == "/":
            body = self.render_index_html().encode("utf-8")
            return Response(
                200, "OK",
                headers=[
                    ("Date", formatdate(usegmt=True)),
                    ("Server", self._server_name),
                    ("Content-Type", "text/html; charset=utf-8"),
                    ("Content-Length", str(len(body))),
                    ("Connection", "close"),
                ],
                body=body,
            )

        if req.method == "POST" and req.path == "/submit":
            params: dict[str, list[str]] = {}

            ctype = req.headers.get("content-type", "")
            body = req.body() or b""
            if ctype.split(";", 1)[0].strip().lower() == "application/x-www-form-urlencoded":

                form = parse_qs(body.decode("utf-8", errors="replace"), keep_blank_values=True)
                params.update(form)

            for k, v in req.query.items():
                params.setdefault(k, []).extend(v)

            subject = (params.get("subject", [""])[0]).strip()
            grade = (params.get("grade", [""])[0]).strip()
            if not subject or not grade:
                raise HTTPError(400, "Bad Request", "Both 'subject' and 'grade' are required")

            # Add grade to the subject's list
            if subject not in GRADES:
                GRADES[subject] = []
            GRADES[subject].append(grade)

            # Post/Redirect/Get: redirect to index after successful POST
            return Response(
                303, "See Other",
                headers=[
                    ("Date", formatdate(usegmt=True)),
                    ("Server", self._server_name),
                    ("Location", "/"),
                    ("Content-Length", "0"),
                    ("Connection", "close"),
                ],
                body=b"",
            )

        raise HTTPError(404, "Not Found")

    def send_response(self, conn: socket.socket, resp: Response):
        # 6. Отправка ответа: status line + headers + CRLF + body
        wfile = conn.makefile("wb")
        status_line = f"HTTP/1.1 {resp.status} {resp.reason}\r\n"
        wfile.write(status_line.encode("iso-8859-1"))
        for (k, v) in resp.headers:
            header_line = f"{k}: {v}\r\n"
            wfile.write(header_line.encode("iso-8859-1"))
        wfile.write(b"\r\n")
        if resp.body:
            wfile.write(resp.body)
        wfile.flush()

    def send_error(self, conn: socket.socket, err: Exception):
        """Uniform error path mirroring the guide: map exceptions to an HTTP response."""
        if isinstance(err, HTTPError):
            status, reason, body_text = err.status, err.reason, err.body
        else:
            status, reason, body_text = 500, "Internal Server Error", "Internal Server Error"
        body = body_text.encode("utf-8")
        resp = Response(
            status, reason,
            headers=[
                ("Date", formatdate(usegmt=True)),
                ("Server", self._server_name),
                ("Content-Type", "text/plain; charset=utf-8"),
                ("Content-Length", str(len(body))),
                ("Connection", "close"),
            ],
            body=body,
        )
        try:
            self.send_response(conn, resp)
        except Exception:
            pass

    def render_index_html(self) -> str:
        if not GRADES:
            rows = "<tr><td colspan='2' style='color:#777'>no records yet</td></tr>"
        else:
            rows = "\n".join(
                f"<tr><td>{self._esc(subject)}</td><td>{', '.join(self._esc(grade) for grade in grades)}</td></tr>"
                for subject, grades in GRADES.items()
            )

        return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Grades</title>
  <style>
    body {{ font: 16px/1.4 system-ui, -apple-system, Segoe UI, Roboto, sans-serif; padding: 2rem; }}
    table {{ border-collapse: collapse; width: 100%; max-width: 640px; }}
    th, td {{ border: 1px solid #ccc; padding: .5rem .75rem; text-align: left; }}
    th {{ background: #f6f6f6; }}
    form {{ margin-top: 1.25rem; max-width: 640px; }}
    input, button {{ font: inherit; padding: .5rem .6rem; }}
    label {{ display:block; margin:.4rem 0 .25rem; }}
  </style>
</head>
<body>
  <h1>Grades</h1>
  <table>
    <thead><tr><th>Subject</th><th>Grade</th></tr></thead>
    <tbody>
      {rows}
    </tbody>
  </table>
  <form method="POST" action="/submit">
    <h2>Add a record</h2>
    <label for="subject">Subject</label>
    <input id="subject" name="subject" required />
    <label for="grade">Grade</label>
    <input id="grade" name="grade" required />
    <div style="margin-top:.8rem">
      <button type="submit">Save</button>
    </div>
  </form>
</body>
</html>"""

    @staticmethod
    def _esc(s: str) -> str:
        return (
            s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;")
             .replace("'", "&#39;")
        )


if __name__ == "__main__":

    serv = MyHTTPServer(HOST, PORT, NAME)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping...")
