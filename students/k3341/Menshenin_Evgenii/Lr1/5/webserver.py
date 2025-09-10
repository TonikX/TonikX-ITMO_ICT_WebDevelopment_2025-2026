import socket

from lesson import *
from request import *


class MyHTTPServer:
    # Параметры сервера
    def __init__(self, host, port, server_name):
        self._host = host
        self._port = port
        self._server_name = server_name
        self.lessons = Lessons()

    def serve_forever(self):
        # 1. Запуск сервера на сокете, обработка входящих соединений
        serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)

        try:
            serv_sock.bind((self._host, self._port))
            serv_sock.listen()

            while True:
                conn, _ = serv_sock.accept()
                try:
                    self.serve_client(conn)
                except Exception as e:
                    print('Client serving failed', e)
        finally:
            serv_sock.close()

    def serve_client(self, conn):
        # 2. Обработка клиентского подключения
        try:
            req = self.parse_request(conn)
            resp = self.handle_request(req)
            self.send_response(conn, resp)
        except ConnectionResetError:
            conn = None
        except Exception as e:
            print('Client serving failed', e)

        if conn:
            conn.close()

    def parse_request(self, conn) -> Request:
        # 3. функция для обработки заголовка http+запроса.
        # Python, сокет предоставляет возможность создать вокруг него некоторую обертку,
        # которая предоставляет file object интерфейс. Это дайте возможность построчно обработать запрос.
        # Заголовок всегда - первая строка. Первую строку нужно разбить на 3 элемента  (метод + url + версия протокола).
        # URL необходимо разбить на адрес и параметры
        # (isu.ifmo.ru/pls/apex/f?p=2143 , где isu.ifmo.ru/pls/apex/f, а p=2143 - параметр p со значением 2143)
        buffer = b''
        while b'\r\n' not in buffer:
            buffer += conn.recv(1)
        buffer = buffer.decode().split(" ")

        headers = self.parse_headers(conn)
        content = self.parse_content(conn, headers)
        url_params = buffer[1].split("?")
        if len(url_params) == 1:
            url_params_dict = {}
        else:
            url_params_dict = {}

            for i in url_params[1].split("&"):
                i = i.split("=")
                url_params_dict[i[0]] = i[1]

        return Request(buffer[0], buffer[1].split("?")[0], buffer[2], url_params_dict, headers, content)

    @staticmethod
    def parse_headers(conn) -> Dict[str, str]:
        # 4. Функция для обработки headers.
        # Необходимо прочитать все заголовки после первой строки до появления пустой строки и сохранить их в массив.
        headers = {}

        while True:
            buffer = b''
            while b'\r\n' not in buffer:
                buffer += conn.recv(1)
            line = buffer.decode().split(": ")
            if line[0] == '\r\n':
                break
            headers[line[0].lower()] = line[1]

        return headers

    def handle_request(self, req: Request) -> Response:
        # 5. Функция для обработки url в соответствии с нужным методом.
        # В случае данной работы, нужно будет создать набор условий, который обрабатывает GET или POST запрос.
        # GET запрос должен возвращать данные. POST запрос должен записывать данные на основе переданных параметров.
        if req.method == "GET" and req.url == "/grades":
            return parse_get_grades_req(self.lessons, req)
        elif req.method == "POST" and req.url == "/grades":
            return parse_set_grades_req(self.lessons, req)
        else:
            return Response(404, "Not Found")

    @staticmethod
    def parse_content(conn, headers) -> Optional[str]:
        if "content-length" not in headers.keys():
            return None

        output = conn.recv(int(headers['content-length']))
        return output.decode()

    @staticmethod
    def send_response(conn, resp: Response):
        # 6. Функция для отправки ответа. Необходимо записать в соединение status line вида HTTP/1.1 <status_code> <reason>.
        # Затем, построчно записать заголовки и пустую строку, обозначающую конец секции заголовков.
        output = f"{resp.http_version} {resp.status} {resp.reason}\r\n\r\n{resp.body}"
        wfile = conn.makefile('wb')
        wfile.write(output.encode())


if __name__ == '__main__':
    host = "localhost"
    port = 8081
    name = 'name'
    serv = MyHTTPServer(host, port, name)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        pass
