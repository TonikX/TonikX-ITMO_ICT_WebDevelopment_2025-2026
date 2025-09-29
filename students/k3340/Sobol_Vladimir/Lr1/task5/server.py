import socket
import urllib.parse
import os

class MyHTTPServer:
    def __init__(self, host, port, name="MyHTTPServer"):
        self.host = host
        self.port = port
        self.name = name
        self.grades = {
            "математика": ["3" , "2"],
        }


        # загружаем HTML-шаблон один раз
        with open("template.html", "r", encoding="utf-8") as f:
            self.template = f.read()

    def render(self, message=""):
        # формируем список оценок
        grades_html = "".join(
    f"<li>{subj}: {', '.join(map(str, grades))}</li>"
    for subj, grades in self.grades.items()
)

        # подставляем в шаблон
        page = self.template.replace("{{grades}}", grades_html or "<li>Пока пусто</li>")
        page = page.replace("{{message}}", message)
        return page

    def serve_forever(self):
        # запуск сервера 
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # SO_REUSEADDR для того чтобы сразу перезагружать сервер и не ждать освобождения порта 
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"{self.name} запущен на {self.host}:{self.port}")

        try:
            while True:
                conn, addr = server_socket.accept()
                self.serve_client(conn, addr)
        finally:
            server_socket.close()

    def serve_client(self, conn, addr):
        # обработчик клиента 
        try:
            # читаем первую строку, заголовки и тело через parse_request
            request_line, headers, body = self.parse_request(conn)
            if not request_line:
                return

            method, url, version = request_line.split()

            # Отдаём CSS
            if url == "/style.css":
                with open("style.css", "r", encoding="utf-8") as f:
                    css = f.read()
                self.send_response(conn, "200 OK", css, content_type="text/css")
                return

            if method == "GET":
                self.handle_get(conn)
            elif method == "POST":
                self.handle_post(conn, body)
            else:
                self.send_response(conn, "405 Method Not Allowed", "<h1>405 Method Not Allowed</h1>")

        except Exception as e:
            self.send_response(conn, "500 Internal Server Error", f"<h1>500 Error</h1><p>{e}</p>")
        finally:
            conn.close()
        

    def parse_request(self, conn):
        f = conn.makefile("rwb", buffering=0)
        request_line = f.readline().decode("utf-8").strip()
        if not request_line:
            return None, {}, ""

        headers = {}
        while True:
            line = f.readline().decode("utf-8").strip()
            if not line:
                break
            key, value = line.split(":", 1)
            headers[key.strip().lower()] = value.strip()

        body = ""
        if "content-length" in headers:
            length = int(headers["content-length"])
            body = f.read(length).decode("utf-8")

        return request_line, headers, body

    def handle_get(self, conn, message=""):
        page = self.render(message)
        self.send_response(conn, "200 OK", page)

    def handle_post(self, conn, body):
        # парсим тело запроса (subject=математика&grade=5 -> {"subject": ["математика"], "grade": ["5"]})
        params = urllib.parse.parse_qs(body)
        # берём предмет (если нет значения, то пустая строка)
        subject = params.get("subject", [""])[0]
        # берем оценку 
        grade = params.get("grade", [""])[0]

        # если предмет и оценка заполнены 
        if subject and grade:
            # сохраняем/обновляем запись в словаре
            if subject not in self.grades:
                self.grades[subject] = []
            self.grades[subject].append(grade)
            
            page = self.render(f"Оценка по '{subject}' обновлена: {grade}")
            self.send_response(conn, "200 OK", page)
        else:
            self.send_response(conn, "400 Bad Request", "<h1>400 Bad Request</h1>")

    def send_response(self, conn, status, body, content_type="text/html"):
        response = (
            f"HTTP/1.1 {status}\r\n"
            f"Content-Type: {content_type}; charset=UTF-8\r\n"
            f"Content-Length: {len(body.encode('utf-8'))}\r\n"
            "Connection: close\r\n"
            "\r\n"
            f"{body}"
        )
        conn.sendall(response.encode("utf-8"))


if __name__ == "__main__":
    serv = MyHTTPServer("localhost", 8081, "GradesServer")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен.")
