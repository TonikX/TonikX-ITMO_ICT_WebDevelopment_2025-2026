import socket
import threading
from urllib.parse import parse_qs


class SimpleHTTPServer:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.grades = {}  # Словарь для хранения оценок {дисциплина: оценка}
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.lock = threading.Lock()  # Для потокобезопасности

    def handle_request(self, client_socket):
        """Обрабатывает HTTP-запрос"""
        request_data = client_socket.recv(4096).decode('utf-8')

        if not request_data:
            client_socket.close()
            return

        # Парсим запрос
        lines = request_data.split('\r\n')
        request_line = lines[0]
        parts = request_line.split(' ')
        if len(parts) < 3:
            client_socket.close()
            return

        method, path, _ = parts

        # Обрабатываем GET и POST запросы
        if method == 'GET' and path == '/':
            self.handle_get_request(client_socket)

        elif method == 'POST' and path == '/add':
            # тело post преобразуем, тк оно приходит единым ответом
            if "\r\n\r\n" in request_data:
                headers, body = request_data.split("\r\n\r\n", 1)
            else:
                body = ""

            post_data = parse_qs(body)
            print(f"Тело запроса: '{body}'")
            print(f"Парсинг данных: {post_data}")

            self.handle_post_request(client_socket, post_data)

        else:
            self.send_response(client_socket, '404 Not Found', 'text/html', '<h1>404 Not Found</h1>')

        client_socket.close()

    def handle_get_request(self, client_socket):
        """Обрабатывает GET-запрос - возвращает HTML-страницу с оценками"""
        html_content = self.generate_html()
        self.send_response(client_socket, '200 OK', 'text/html', html_content)

    def handle_post_request(self, client_socket, post_data):
        """Обрабатывает POST-запрос - добавляет новую оценку"""
        # Извлекаем данные
        discipline = post_data.get('discipline', [''])[0].strip()
        grade = post_data.get('grade', [''])[0].strip()

        print(f"Извлеченные данные - Дисциплина: '{discipline}', Оценка: '{grade}'")

        if discipline and grade:
            with self.lock:
                # Сохраняем данные
                self.grades[discipline] = grade
                print(f"Сохранено: {discipline} - {grade}")
                print(f"Все оценки: {self.grades}")

            # Перенаправляем на главную страницу
            self.send_redirect(client_socket, '/')
        else:
            error_msg = f"Ошибка: не получены все данные. Дисциплина: '{discipline}', Оценка: '{grade}'"
            print(error_msg)
            self.send_response(client_socket, '400 Bad Request', 'text/html',
                               f'<h1>400 Bad Request</h1><p>{error_msg}</p>')

    def generate_html(self):
        """Генерирует HTML-страницу с формой и таблицей оценок"""
        html = """
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <title>Учет оценок</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                table { border-collapse: collapse; width: 100%; margin-top: 20px; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                form { margin-bottom: 20px; }
                input[type=text], input[type=number] { padding: 8px; margin: 5px; }
                input[type=submit] { padding: 8px 16px; background-color: #4CAF50; color: white; border: none; }
            </style>
        </head>
        <body>
            <h1>Система учета оценок</h1>

            <form method="POST" action="/add">
                <h2>Добавить новую оценку</h2>
                <div>
                    <label>Дисциплина:</label>
                    <input type="text" name="discipline" required>
                </div>
                <div>
                    <label>Оценка:</label>
                    <input type="number" name="grade" min="1" max="5" required>
                </div>
                <input type="submit" value="Добавить">
            </form>

            <h2>Список оценок</h2>
            <table>
                <tr>
                    <th>Дисциплина</th>
                    <th>Оценка</th>
                </tr>
        """

        # Добавляем строки таблицы с оценками
        with self.lock:
            for discipline, grade in self.grades.items():
                html += f"""
                <tr>
                    <td>{discipline}</td>
                    <td>{grade}</td>
                </tr>
                """

        html += """
            </table>
        </body>
        </html>
        """

        return html

    def send_response(self, client_socket, status, content_type, content):
        """Отправляет HTTP-ответ"""
        body = content.encode('utf-8')  # кодируем заранее
        response = f"HTTP/1.1 {status}\r\n"
        response += "Content-Type: text/html; charset=utf-8\r\n"
        response += f"Content-Length: {len(body)}\r\n"
        response += "Connection: close\r\n"
        response += "\r\n"

        client_socket.sendall(response.encode('utf-8') + body)

    def send_redirect(self, client_socket, location):
        """Отправляет перенаправление"""
        response = f"HTTP/1.1 302 Found\r\n"
        response += f"Location: {location}\r\n"
        response += "Connection: close\r\n"
        response += "\r\n"

        client_socket.sendall(response.encode('utf-8'))

    def start(self):
        """Запускает сервер"""
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Веб-сервер запущен на http://{self.host}:{self.port}")

        try:
            while True:
                client_socket, client_address = self.server_socket.accept()
                print(f"Подключение от {client_address}")

                # Обрабатываем запрос в отдельном потоке
                thread = threading.Thread(target=self.handle_request, args=(client_socket,))
                thread.daemon = True
                thread.start()

        except KeyboardInterrupt:
            print("\nОстановка сервера...")
        finally:
            self.server_socket.close()


if __name__ == "__main__":
    server = SimpleHTTPServer()
    server.start()