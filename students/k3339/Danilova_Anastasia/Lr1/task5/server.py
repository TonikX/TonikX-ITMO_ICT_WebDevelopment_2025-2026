import socket
from templates import get_main_page, get_success_page, get_error_page

class MyHTTPServer:
    def __init__(self, host='127.0.0.1', port=8889):
        self.host = host
        self.port = port
        self.grades = {}

    def serve_forever(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        sock.listen(5)
        print(f"Server running at http://{self.host}:{self.port}  (CTRL+C to stop)")

        try:
            while True:
                conn, addr = sock.accept()
                try:
                    self.serve_client(conn)
                except Exception as e:
                    print("Error handling client:", e)
                finally:
                    conn.close()
        except KeyboardInterrupt:
            print("\nServer stopped by user")
        finally:
            sock.close()

    def serve_client(self, conn):
        # чтение заголовков запроса
        request_head = b""
        while b"\r\n\r\n" not in request_head:
            chunk = conn.recv(1024)
            if not chunk:
                break
            request_head += chunk

        if not request_head:
            return
        # если в байтах встречается некорректная UTF-8 последовательность заменить её символом замены
        head_str = request_head.decode('utf-8', errors='replace')

        # разбитие заголовочной части
        head_lines = head_str.split("\r\n")
        request_line = head_lines[0]
        parts = request_line.split()
        # не формат HTTP
        if len(parts) != 3:
            self.send_response(conn, 400, "Bad Request", get_error_page("Malformed request line", 400))
            return

        method, path, protocol = parts

        # парсинг заголовоков в словарь
        headers = {}
        for line in head_lines[1:]:
            if not line:
                break
            if ':' in line:
                k, v = line.split(':', 1)
                headers[k.strip().lower()] = v.strip()

        body = ""
        if method.upper() == 'POST':
            content_length = int(headers.get('content-length', '0'))
            split_index = head_str.find("\r\n\r\n")
            if split_index != -1:
                already = head_str[split_index+4:]
                body_bytes = already.encode('utf-8', errors='replace')
            else:
                body_bytes = b""

            remaining = content_length - len(body_bytes)
            while remaining > 0:
                chunk = conn.recv(1024)
                if not chunk:
                    break
                body_bytes += chunk
                remaining -= len(chunk)

            try:
                body = body_bytes.decode('utf-8', errors='replace')
            except:
                body = ""

        req = {
            'method': method.upper(),
            'path': path,
            'protocol': protocol,
            'headers': headers,
            'body': body
        }

        # обработка запроса
        try:
            if req['method'] == 'GET':
                html = get_main_page(self.grades)
                self.send_response(conn, 200, "OK", html)
            elif req['method'] == 'POST':
                if not req['body']:
                    self.send_response(conn, 400, "Bad Request", get_error_page("Empty POST body", 400))
                    return

                params = self.parse_form_data(req['body'])
                discipline = params.get('discipline', '').strip()
                grade = params.get('grade', '').strip()

                if not discipline or not grade:
                    self.send_response(conn, 400, "Bad Request", get_error_page("Discipline and grade are required", 400))
                    return

                if not grade.isdigit() or not (1 <= int(grade) <= 5):
                    self.send_response(conn, 400, "Bad Request", get_error_page("Grade must be an integer from 1 to 5", 400))
                    return


                if discipline in self.grades:
                    old = self.grades[discipline]
                    self.grades[discipline] = grade
                    message = f"Grade for '{discipline}' updated: {old} → {grade}"
                else:
                    self.grades[discipline] = grade
                    message = f"Discipline '{discipline}' with grade {grade} added!"

                html = get_success_page(message)
                self.send_response(conn, 200, "OK", html)
            else:
                self.send_response(conn, 405, "Method Not Allowed", get_error_page("Only GET and POST are supported", 405))
        except Exception as e:

            self.send_response(conn, 500, "Internal Server Error", get_error_page(str(e), 500))

    def parse_form_data(self, body):
        """
        парсер из тела POST
        """
        params = {}
        for pair in body.split('&'):
            if '=' in pair:
                k, v = pair.split('=', 1)
                params[k] = v
        return params

    def send_response(self, conn, code, reason, body_html):
        body_bytes = body_html.encode('utf-8')
        resp_lines = [
            f"HTTP/1.1 {code} {reason}",
            "Content-Type: text/html; charset=utf-8",
            f"Content-Length: {len(body_bytes)}",
            "Connection: close",
            "",
            ""
        ]
        header = "\r\n".join(resp_lines).encode('utf-8')
        conn.sendall(header + body_bytes)


if __name__ == "__main__":
    srv = MyHTTPServer(host='127.0.0.1', port=8889)
    srv.serve_forever()
