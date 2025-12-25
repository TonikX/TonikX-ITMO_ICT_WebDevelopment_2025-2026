from io import IOBase
import socket
from urllib.parse import parse_qs, urlparse 
from code.config import BUFFER, ENCODING

class MyHTTPServer:

    def __init__(self, host: str, port: int, name: str) -> None:
        self.name = name
        self.host = host
        self.port = port
        self.grades = {}
  
    def serve_forever(self):
        # 1. Запуск сервера на сокете, обработка входящих соединений
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        while True:
            conn, _ = server_socket.accept()
            self.serve_client(conn)
            conn.close()
        

    def serve_client(self, conn: socket.socket):
        # 2. Обработка клиентского подключения
        f = conn.makefile(mode="rw", buffering=BUFFER, encoding=ENCODING)
        method, path, version, headers, querry_params = self.parse_request(f=f)
        self.handle_request(f=f, method=method, path=path, version=version, headers=headers,querry_params=querry_params)
        

    def parse_request(self, f: IOBase):
        # 3. функция для обработки заголовка http+запроса. Python, сокет предоставляет возможность создать вокруг него некоторую обертку, которая предоставляет file object интерфейс. Это дайте возможность построчно обработать запрос. Заголовок всегда - первая строка. Первую строку нужно разбить на 3 элемента  (метод + url + версия протокола). URL необходимо разбить на адрес и параметры (isu.ifmo.ru/pls/apex/f?p=2143 , где isu.ifmo.ru/pls/apex/f, а p=2143 - параметр p со значением 2143)
        method, path, version, headers, querry_params = self.parse_headers(f)
        return method, path, version, headers, querry_params



    def parse_headers(self, f: IOBase):
        # 4. Функция для обработки headers. Необходимо прочитать все заголовки после первой строки до появления пустой строки и сохранить их в массив.
        request_line = f.readline()
        if not request_line:
            f.close()

        method, url, version = request_line.split(" ", 2)
        headers = {}
        while True:
            header = f.readline()
            if header in ("\r\n", "\n", ""):
                break
            name, value = header.split(":", 1)
            headers[name.strip()] = value.strip()
        
        parsed = urlparse(url)
        path = parsed.path
        querry_params = parse_qs(parsed.query)
        return method, path, version, headers, querry_params


    def handle_request(self, f: IOBase, method: str, path: str, version: str,
                       headers: dict, querry_params: dict):
        # self.grades предполагается как список словарей: [{'discipline':..., 'grade':...}]

        if method == "POST":
            # --- здесь мы берём данные, пришедшие от клиента ---
            # discipline и grade приходят как параметры формы
            discipline = querry_params.get('discipline', [''])[0]
            grade = querry_params.get('grade', [''])[0]

            # --- здесь добавляем в нашу "базу" ---
            if discipline and grade:
                if discipline not in self.grades.keys():
                    self.grades[discipline] = [grade]
                else:
                    self.grades[discipline].append(grade)
                response_headers = (
                    f"{version} 200 OK\r\n"
                    "\r\n"
                )
                self.send_response(f=f, response_headers=response_headers)
           
        elif method == "GET":
            # --- формируем HTML таблицу на основе self.grades ---
            rows = "".join(
                f"<tr><td>{g}</td><td>{self.grades[g]}</td></tr>"
                for g in self.grades.keys()
            )

            html = f"""
            <html>
            <head><title>Grades</title></head>
            <body>
                <h1>Grades</h1>
                <table border="1">
                    <tr><th>Discipline</th><th>Grade</th></tr>
                    {rows}
                </table>
            </body>
            </html>
            """

            # --- здесь формируем HTTP-ответ с заголовками ---
            response_headers = (
                f"{version} 200 OK\r\n"
                "Content-Type: text/html; charset=utf-8\r\n"
                f"Content-Length: {len(html)}\r\n"
                "\r\n"
            )
            self.send_response(f=f, response_headers=response_headers, body=html)



    def send_response(self, f: IOBase, response_headers: str, body=None):
        # 6. Функция для отправки ответа. Необходимо записать в соединение status line вида HTTP/1.1 <status_code> <reason>. Затем, построчно записать заголовки и пустую строку, обозначающую конец секции заголовков.
        if body:
            f.write(response_headers + body)
            f.flush()
            f.close()
        else:
            f.write(response_headers)
            f.flush()
            f.close()

