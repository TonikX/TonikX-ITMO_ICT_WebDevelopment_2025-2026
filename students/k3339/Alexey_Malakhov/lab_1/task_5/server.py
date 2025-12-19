import socket
from urllib.parse import unquote


class MyHTTPServer:
    def __init__(self, host, port, server_name):
        self._host = host
        self._port = port
        self._server_name = server_name
        self.database = {}

    def serve_forever(self):
        serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
        serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Разрешить повторное использование порта

        try:
            serv_sock.bind((self._host, self._port))
            serv_sock.listen()
            print(f"Сервер запущен на {self._host}:{self._port}")

            while True:
                conn, _ = serv_sock.accept()
                try:
                    self.serve_client(conn)
                except Exception as e:
                    print('Client serving failed', e)
        finally:
            serv_sock.close()

    def serve_client(self, conn):
        try:
            req = self.parse_request(conn)
            resp = self.handle_request(req)
            self.send_response(conn, resp)
        except ConnectionResetError:
            conn = None
        except Exception as e:
            self.send_error(conn, e)

        if conn:
            conn.close()

    def parse_request(self, conn):
        raw_data = conn.recv(1024).decode('utf-8')
        params = {}
        headers = {}

        lines = raw_data.split('\r\n')

        request_header = lines[0]
        method, url, ver = request_header.split()
        if '?' in url:
            adress, raw_params = url.split('?')
            for param in raw_params.split('&'):
                name, value = param.split('=')
                params[name] = unquote(value.replace('+', ' '))
        else:
            adress = url
            params = None

        body_found = False
        for i, header in enumerate(lines[1:], 1):
            if header == '':
                body_found = True
                if method == 'POST' and i + 1 < len(lines):
                    body = ''.join(lines[i + 1 :])
                    params = {}

                    for param in body.split('&'):
                        if '=' in param:
                            name, value = param.split('=')
                            params[name] = unquote(value.replace('+', ' '))
                break
            elif ': ' in header:
                name, value = header.split(': ')
                headers[name] = value

        return {'method': method, 'path': adress, 'params': params, 'headers': headers, 'version': ver}

    def handle_request(self, req):
        method = req['method']
        params = req['params']
        message = ""

        if method == 'POST':
            if params and 'key' in params and 'value' in params:
                key = params['key']
                value = params['value']

                if key and value:
                    self.database.setdefault(key, []).append(value)
                    message = f'<p>Добавлено: {key} = {value}</p>'
                    print(self.database)
                else:
                    message = '<p>Ошибка: Все поля обязательны!</p>'
            else:
                message = '<p>Ошибка: Данные не получены!</p>'

        # Генерируем строки таблицы
        table_rows = ""
        if self.database:
            for key, value in self.database.items():
                table_rows += f'<tr><td>{key}</td><td>{" ".join(value)}</td></tr>'
        else:
            table_rows = '<tr><td colspan="2">База данных пуста</td></tr>'

        html_base = f'''
            <!doctype html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <title>Простой сервер на Python</title>
                </head>
                <body>
                    <h1>Учебный журнал</h1>
                    {message}
                
                    <table border="1">
                        <tr>
                            <th>Дисциплина</th>
                            <th>Оценки</th>
                        </tr>
                        {table_rows}
                    </table>
                    
                    <form method="POST" action="/">
                        <input type="text" name="key" placeholder="Дисциплина" required>
                        <input type="text" name="value" placeholder="Оценки" required>

                        <button type="submit">Отправить</button>
                    </form>
                </body>
                </html>
                '''

        return html_base

    def send_response(self, conn, resp):
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(resp.encode('utf-8'))}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )
        response += resp
        conn.sendall(response.encode('utf-8'))  # UTF-8 encoding

    def send_error(self, conn, err):
        error_response = (
            "HTTP/1.1 500 Internal Server Error\r\n"
            "Content-Type: text/plain; charset=utf-8\r\n"
            "Connection: close\r\n"
            "\r\n"
            f"Error: {str(err)}"
        )

        try:
            conn.sendall(error_response.encode('utf-8'))
        except:
            pass


if __name__ == '__main__':
    host = 'localhost'
    port = 3333
    name = 'test'
    serv = MyHTTPServer(host, port, name)
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        pass
