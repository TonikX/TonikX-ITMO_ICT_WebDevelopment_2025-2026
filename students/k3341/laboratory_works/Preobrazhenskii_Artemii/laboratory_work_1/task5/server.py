import socket
import sys


class GradesServer:
    def __init__(self, host, port, server_name):
        self._host = host
        self._port = port
        self._server_name = server_name
        self.data = {}

    def serve_forever(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sock:
            serv_sock.bind((self._host, self._port))
            serv_sock.listen()
            print(f"Server running at http://{self._host}:{self._port}/")
            while True:
                conn, _ = serv_sock.accept()
                with conn:
                    try:
                        self.serve_client(conn)
                    except ValueError as e:
                        self.send_error(conn, 400, "Bad Request", str(e))
                    except NotImplementedError as e:
                        self.send_error(conn, 405, "Method Not Allowed", str(e))
                    except Exception as e:
                        print("Client serving failed:", e)
                        self.send_error(conn, 500, "Internal Server Error", str(e))

    def serve_client(self, conn):
        req = self.parse_request(conn)
        resp = self.handle_request(req)
        conn.sendall(resp.encode("utf-8"))

    def parse_request(self, conn):
        req = conn.recv(1024).decode()
        lines = req.splitlines()
        if not lines:
            raise ValueError("Empty request")
        # разбиваем 1 строку запросу (к примеру POST / HTTP/1.1)
        method, path = lines[0].split()[:2]
        # тело запроса, есть метод post, иначе пустое
        body = lines[-1] if method.upper() == "POST" else ""
        return {"method": method.upper(), "path": path, "body": body}

    def handle_request(self, req):
        if req["method"] == "POST":
            params = {}
            for part in req["body"].split("&"):
                if "=" not in part:
                    raise ValueError("Неверный формат параметров")
                key, value = part.split("=", 1)
                params[key] = value

            if "discipline" not in params or "grade" not in params:
                raise ValueError("Отсутствуют обязательные параметры")

            if not params["grade"].isdigit():
                raise ValueError("Оценка должна быть числом")

            discipline = params["discipline"]
            grade = params["grade"]
            
            if discipline not in self.data:
                self.data[discipline] = []

            self.data[discipline].append(grade)
            return self.build_html()

        elif req["method"] == "GET":
            return self.build_html()
        else:
            raise NotImplementedError(f"Метод {req['method']} не поддерживается")

    def http_response(self, code, reason, body):
        return f"HTTP/1.1 {code} {reason}\r\n" \
               f"Content-Type: text/html; charset=utf-8\r\n" \
               f"Content-Length: {len(body.encode('utf-8'))}\r\n\r\n{body}"

    def build_html(self):
        items = ""
        for discipline, grades in self.data.items():
            grades_str = ", ".join(grades)  # все оценки через запятую
            items += f"<li>{discipline}: {grades_str}</li>"
        html = f"<html><head><title>Grades</title></head><body><h2>Все оценки</h2><ul>{items}</ul></body></html>"
        return self.http_response(200, "OK", html)

    def send_error(self, conn, code, reason, message):
        body = f"<h1>{code} {reason}</h1><p>{message}</p>"
        resp = self.http_response(code, reason, body)
        conn.sendall(resp.encode("utf-8"))

if __name__ == "__main__":
    host = sys.argv[1]
    port = int(sys.argv[2])
    name = sys.argv[3]
    GradesServer(host, port, name).serve_forever()