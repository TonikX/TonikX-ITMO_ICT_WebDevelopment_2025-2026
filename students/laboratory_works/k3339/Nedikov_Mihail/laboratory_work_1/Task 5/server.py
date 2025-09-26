import socket
import sys
from email.parser import Parser
from functools import lru_cache
from urllib.parse import parse_qs, urlparse
import threading
import json
import os

MAX_LINE = 64 * 1024
MAX_HEADERS = 100
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "grades.json")


class MyHTTPServer:
    def __init__(self, host, port, server_name):
        """Сохраняет настройки сервера и загружает сохранённые данные."""
        self._host = host
        self._port = port
        self._server_name = server_name
        self._subjects = {}  # id -> {"id": int, "title": str, "grades": [str]}
        self._lock = threading.Lock()
        self._load_data()

    def _load_data(self):
        """Читает сохранённые предметы из JSON-файла на диске."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self._subjects = {item["id"]: item for item in data}
            except (OSError, json.JSONDecodeError) as err:
                print("Failed to load saved data:", err)

    def _save_data(self):
        """Сохраняет текущий список предметов в файл JSON."""
        with self._lock:
            data = list(self._subjects.values())
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

    def serve_forever(self):
        """Запускает бесконечный цикл приёма и обработки подключений."""
        serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
        serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            serv_sock.bind((self._host, self._port))
            serv_sock.listen()
            print(f"Serving on {self._host}:{self._port} ...")

            while True:
                conn, _ = serv_sock.accept()
                threading.Thread(
                    target=self.serve_client, args=(conn,), daemon=True
                ).start()
        finally:
            serv_sock.close()

    def serve_client(self, conn):
        """Обрабатывает одного клиента: парсит запрос, формирует ответ."""
        try:
            req = self.parse_request(conn)
            resp = self.handle_request(req)
            self.send_response(conn, resp)
        except ConnectionResetError:
            pass
        except HTTPError as err:
            self.send_error(conn, err)
        except Exception as err:
            self.send_error(conn, HTTPError(500, "Internal Server Error", str(err)))
        finally:
            conn.close()

    def parse_request(self, conn):
        """Создаёт объект Request из сырых данных сокета."""
        rfile = conn.makefile("rb")
        method, target, ver = self.parse_request_line(rfile)
        headers = self.parse_headers(rfile)
        host = headers.get("Host")
        if not host:
            raise HTTPError(400, "Bad Request", "Host header required")
        return Request(method, target, ver, headers, rfile)

    def parse_request_line(self, rfile):
        """Читает первую строку HTTP-запроса и разбивает её на части."""
        raw = rfile.readline(MAX_LINE + 1)
        if len(raw) > MAX_LINE:
            raise HTTPError(414, "Request URI Too Long", "Request line is too long")
        req_line = str(raw, "iso-8859-1").rstrip("\r\n")
        words = req_line.split()
        if len(words) != 3:
            raise HTTPError(400, "Bad Request", "Malformed request line")
        method, target, ver = words
        if ver != "HTTP/1.1":
            raise HTTPError(505, "HTTP Version Not Supported", "Unexpected HTTP version")
        return method, target, ver

    def parse_headers(self, rfile):
        """Собирает заголовки HTTP-запроса в объект email.message."""
        headers = []
        while True:
            line = rfile.readline(MAX_LINE + 1)
            if len(line) > MAX_LINE:
                raise HTTPError(431, "Request Header Fields Too Large", "Header line is too long")
            if line in (b"\r\n", b"\n", b""):
                break
            headers.append(line)
            if len(headers) > MAX_HEADERS:
                raise HTTPError(431, "Request Header Fields Too Large", "Too many headers")
        sheaders = b"".join(headers).decode("iso-8859-1")
        return Parser().parsestr(sheaders)

    def handle_request(self, req):
        """Маршрутизирует запрос к нужному обработчику."""
        if req.path == "/" and req.method == "GET":
            return self.handle_index(req)
        if req.path == "/set_subject" and req.method == "POST":
            return self.handle_set_subject(req)
        if req.path == "/grades" and req.method == "GET":
            return self.handle_get_grades(req)
        if req.path == "/favicon.ico":
            return Response(
                204, "No Content", [("Content-Length", "0"), ("Connection", "close")]
            )
        raise HTTPError(404, "Not Found", f"No route for {req.method} {req.path}")

    def handle_index(self, req):
        """Отдаёт HTML-страницу с формой и списком оценок."""
        body = "<html><head><title>Grades</title></head><body>"
        body += "<h1>Добавить оценку</h1>"
        body += """
        <form method="POST" action="/set_subject">
          Дисциплина: <input type="text" name="title"><br>
          Оценка: <input type="text" name="grade"><br>
          <input type="submit" value="Добавить">
        </form>
        <hr>
        """
        body += "<h2>Оценки</h2><ul>"
        with self._lock:
            for subj in self._subjects.values():
                grades_str = ", ".join(subj["grades"])
                body += f"<li>{subj['title']}: {grades_str}</li>"
        body += "</ul></body></html>"

        body = body.encode("utf-8")
        headers = [
            ("Content-Type", "text/html; charset=utf-8"),
            ("Content-Length", str(len(body))),
            ("Connection", "close"),
        ]
        return Response(200, "OK", headers, body)

    def handle_set_subject(self, req):
        """Принимает данные формы и обновляет список предметов."""
        q = req.query

        # Если параметры пустые — читаем тело формы
        if req.method == "POST" and not q:
            ctype = req.headers.get("Content-Type", "")
            if "application/x-www-form-urlencoded" in ctype:
                length = int(req.headers.get("Content-Length", 0))
                body = req.rfile.read(length).decode("utf-8")
                q = parse_qs(body)

        try:
            title = q["title"][0]
            grade = q["grade"][0]
        except (KeyError, IndexError):
            raise HTTPError(400, "Bad Request", "title and grade are required")

        with self._lock:
            existing = next(
                (s for s in self._subjects.values() if s["title"] == title), None
            )
            if existing:
                existing["grades"].append(grade)
                subject_id = existing["id"]
            else:
                subject_id = (max(self._subjects.keys()) + 1) if self._subjects else 1
                self._subjects[subject_id] = {
                    "id": subject_id,
                    "title": title,
                    "grades": [grade],
                }

        self._save_data()

        headers = [
            ("Location", "/"),
            ("Content-Length", "0"),
            ("Connection", "close"),
        ]
        return Response(303, "See Other", headers=headers)

    def handle_get_grades(self, req):
        """Возвращает список предметов в формате JSON."""
        with self._lock:
            data = list(self._subjects.values())
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        headers = [
            ("Content-Type", "application/json; charset=utf-8"),
            ("Content-Length", str(len(body))),
            ("Connection", "close"),
        ]
        return Response(200, "OK", headers, body)

    def send_response(self, conn, resp):
        """Формирует HTTP-ответ и отправляет его клиенту."""
        wfile = conn.makefile("wb")
        status_line = f"HTTP/1.1 {resp.status} {resp.reason}\r\n"
        wfile.write(status_line.encode("iso-8859-1"))

        headers = resp.headers or []
        has_len = any(k.lower() == "content-length" for k, _ in headers)
        has_conn = any(k.lower() == "connection" for k, _ in headers)

        if resp.body is not None and not has_len:
            headers.append(("Content-Length", str(len(resp.body))))
        if resp.body is None and not has_len:
            headers.append(("Content-Length", "0"))
        if not has_conn:
            headers.append(("Connection", "close"))

        for k, v in headers:
            wfile.write(f"{k}: {v}\r\n".encode("iso-8859-1"))

        wfile.write(b"\r\n")
        if resp.body is not None:
            wfile.write(resp.body)

        wfile.flush()
        wfile.close()

    def send_error(self, conn, err):
        """Создаёт ответ с ошибкой, если обработка запроса завершилась исключением."""
        try:
            status = getattr(err, "status", 500)
            reason = getattr(err, "reason", "Internal Server Error")
            body_raw = getattr(err, "body", None)

            if body_raw is None:
                body_raw = reason
            if isinstance(body_raw, bytes):
                body = body_raw
            else:
                body = str(body_raw).encode("utf-8")

        except Exception:
            status = 500
            reason = "Internal Server Error"
            body = b"Internal Server Error"

        headers = [
            ("Content-Type", "text/plain; charset=utf-8"),
            ("Content-Length", str(len(body))),
            ("Connection", "close"),
        ]
        resp = Response(status, reason, headers, body)
        self.send_response(conn, resp)


class Request:
    """Обёртка над данными HTTP-запроса с удобными свойствами."""
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


class Response:
    """Простая структура для ответа сервера."""
    def __init__(self, status, reason, headers=None, body=None):
        self.status = status
        self.reason = reason
        self.headers = headers
        self.body = body


class HTTPError(Exception):
    """Исключение для передачи HTTP-статуса и текста ошибки клиенту."""
    def __init__(self, status, reason, body=None):
        super().__init__(reason)
        self.status = status
        self.reason = reason
        self.body = body


if __name__ == "__main__":
    host = sys.argv[1]
    port = int(sys.argv[2])
    name = sys.argv[3]
    serv = MyHTTPServer(host, port, name)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        pass
