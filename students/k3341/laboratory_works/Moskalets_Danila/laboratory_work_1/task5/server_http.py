import socket
import urllib.parse


class MyHTTPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.data = {}  # { "Математика": [5, 4], "Физика": [3] }

    # запуск сервера на сокете, обработка входящих соединений
    def serve_forever(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Сервер запущен на http://{self.host}:{self.port}")

        while True:
            client_socket, addr = server_socket.accept()
            self.serve_client(client_socket)
            client_socket.close()

    # обработка клиентского подключения
    def serve_client(self, client_socket):
        request = client_socket.recv(4096).decode('utf-8')
        if not request:
            return

        # первая строка: метод, путь, версия
        first_line = request.split('\r\n')[0]  # POST / HTTP/1.1
        method, path, _ = first_line.split()

        if method == 'POST':
            body = request.split('\r\n\r\n')[1]  # все, что после пустой строки - тело
            params = urllib.parse.parse_qs(body)  # превращаем в словарь тело http-запроса (subject=Математика&grade=5)
            subject = params.get('subject', [''])[0].strip()
            grade = params.get('grade', [''])[0]

            if subject and grade:
                # если subject нет в словаре - создаем его со значением [] и затем добавляем grade
                self.data.setdefault(subject, []).append(grade)

            self.send_response(client_socket, "HTTP/1.1 303 See Other\r\nLocation: /\r\n\r\n")

        elif method == 'GET':
            html = self.generate_html()
            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=utf-8\r\n"
                f"Content-Length: {len(html.encode('utf-8'))}\r\n"
                "\r\n"
                f"{html}"
            )
            client_socket.sendall(response.encode('utf-8'))

    def generate_html(self):
        rows = ""
        for subj, grades in self.data.items():
            rows += f"<tr><td>{subj}</td><td>{', '.join(grades)}</td></tr>"
        return f"""
        <html>
        <head>
            <meta charset="utf-8">
            <title>Журнал оценок</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f6f8;
                    margin: 0;
                    padding: 20px;
                }}
                h1 {{
                    text-align: center;
                    color: #2c3e50;
                }}
                form {{
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    max-width: 400px;
                    margin: 20px auto;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                }}
                input[type="text"], input[type="number"] {{
                    width: 100%;
                    padding: 8px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    margin-top: 5px;
                    margin-bottom: 10px;
                }}
                input[type="submit"] {{
                    width: 100%;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 10px;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 16px;
                }}
                input[type="submit"]:hover {{
                    background-color: #45a049;
                }}
                table {{
                    margin: 30px auto;
                    border-collapse: collapse;
                    width: 80%;
                    background: white;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 10px;
                    text-align: center;
                }}
                th {{
                    background-color: #4CAF50;
                    color: white;
                }}
                tr:nth-child(even) {{
                    background-color: #f2f2f2;
                }}
            </style>
        </head>
        <body>
            <h1>Журнал оценок</h1>
            <form method="POST">
                <label>Дисциплина:</label>
                <input type="text" name="subject" required>
                <label>Оценка:</label>
                <input type="number" name="grade" min="1" max="5" required>
                <input type="submit" value="Добавить">
            </form>
            <table>
                <tr><th>Дисциплина</th><th>Оценки</th></tr>
                {rows}
            </table>
        </body>
        </html>
        """

    def send_response(self, client_socket, response_text):
        client_socket.sendall(response_text.encode('utf-8'))


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 9090
    server = MyHTTPServer(host, port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен.")
