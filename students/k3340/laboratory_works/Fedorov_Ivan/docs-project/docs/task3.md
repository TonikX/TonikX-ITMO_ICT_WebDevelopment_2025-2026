## Цель

Реализовать серверную часть приложения, которая обрабатывает HTTP-запросы.  
Клиент подключается к серверу и получает в ответ **HTTP-сообщение**, содержащее HTML-страницу, загруженную сервером из файла `index.html`.

## Выполнение

    1) Инициализация сервера: Сервер создаёт сокет и привязывает его к указанному адресу и порту (по умолчанию localhost:8080).

    2) Ожидание подключений: Сервер переходит в режим прослушивания входящих соединений методом listen().

    3) Обработка запросов: При подключении клиента сервер принимает соединение методом accept() и обрабатывает HTTP-запрос.

    4) Чтение HTML-файла: Сервер загружает содержимое файла index.html из текущей директории.

    5) Формирование ответа: На основе полученного запроса и содержимого файла формируется HTTP-ответ с соответствующими заголовками:

        Статус ответа (200 OK, 404 Not Found или 500 Internal Error)

        Content-Type и Content-Length

        Дата и информация о сервере

    6) Отправка ответа: Сформированный HTTP-ответ отправляется клиенту через установленное сокет-соединение.

    7) Завершение соединения: После отправки ответа соединение с клиентом закрывается.

### Сервер

```python
import socket
import os
from datetime import datetime


class HTTPServer:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.socket = None

    def load_html_file(self, filename):
        """Загружает содержимое HTML файла"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            return None

    def create_http_response(self, status_code, content, content_type='text/html; charset=utf-8'):
        """Создает HTTP ответ с правильными заголовками"""
        status_messages = {
            200: 'OK',
            404: 'Not Found',
            500: 'Internal Server Error'
        }

        response = [
            f"HTTP/1.1 {status_code} {status_messages.get(status_code, 'Unknown')}",
            f"Content-Type: {content_type}",
            f"Content-Length: {len(content.encode('utf-8'))}",
            "Connection: close",
            f"Date: {datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')}",
            "Server: CustomPythonHTTPServer/1.0",
            "",  # Пустая строка разделяет заголовки и тело
            content
        ]

        return "\r\n".join(response)

    def handle_request(self, client_socket):
        """Обрабатывает HTTP запрос"""
        try:
            # Получаем данные от клиента
            request_data = client_socket.recv(1024).decode('utf-8')
            print(f"Получен запрос:\n{request_data}")

            # Парсим первую строку запроса
            request_lines = request_data.split('\r\n')
            if not request_lines:
                return

            first_line = request_lines[0]
            method, path, version = first_line.split()

            print(f"Метод: {method}, Путь: {path}")

            # Загружаем HTML файл
            html_content = self.load_html_file('index.html')

            if html_content is None:
                # Если файл не найден
                error_html = """
                <!DOCTYPE html>
                <html>
                <head><title>404 Not Found</title></head>
                <body>
                    <h1>404 - Страница не найдена</h1>
                    <p>Файл index.html не найден на сервере</p>
                </body>
                </html>
                """
                response = self.create_http_response(404, error_html)
            else:
                # Успешный ответ с HTML содержимым
                response = self.create_http_response(200, html_content)

            # Отправляем ответ клиенту
            client_socket.send(response.encode('utf-8'))
            print("Ответ отправлен клиенту")

        except Exception as e:
            print(f"Ошибка при обработке запроса: {e}")
            error_html = """
            <!DOCTYPE html>
            <html>
            <head><title>500 Internal Error</title></head>
            <body>
                <h1>500 - Внутренняя ошибка сервера</h1>
                <p>Произошла ошибка при обработке запроса</p>
            </body>
            </html>
            """
            response = self.create_http_response(500, error_html)
            client_socket.send(response.encode('utf-8'))

    def start(self):
        """Запускает HTTP сервер"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)

            print(f"HTTP сервер запущен на http://{self.host}:{self.port}")
            print("Для остановки сервера нажмите Ctrl+C")
            print("=" * 50)

            while True:
                client_socket, client_address = self.socket.accept()
                print(f"Подключен клиент: {client_address}")

                try:
                    self.handle_request(client_socket)
                except Exception as e:
                    print(f"Ошибка при работе с клиентом {client_address}: {e}")
                finally:
                    client_socket.close()
                    print(f"Соединение с {client_address} закрыто\n")

        except KeyboardInterrupt:
            print("\nСервер остановлен")
        except Exception as e:
            print(f"Ошибка сервера: {e}")
        finally:
            if self.socket:
                self.socket.close()


def main():
    # Проверяем существование файла index.html
    if not os.path.exists('index.html'):
        print("Внимание: файл index.html не найден!")
        print("Создайте файл index.html в той же директории, что и server.py")
        create_example = input("Создать пример index.html? (y/n): ")
        if create_example.lower() == 'y':
            with open('index.html', 'w', encoding='utf-8') as f:
                f.write("""<!DOCTYPE html>
<html>
<head><title>Пример страницы</title></head>
<body>
    <h1>Привет от HTTP сервера!</h1>
    <p>Это пример HTML страницы</p>
</body>
</html>""")
            print("Файл index.html создан!")
        else:
            return

    # Запускаем сервер
    server = HTTPServer()
    server.start()


if __name__ == "__main__":
    main()
```

## Результат

Приведен скриншот страницы, которую отдает сервер браузеру по адресу `127.0.0.1:8080`:

![](assets/task3client.png)

Сервер просто информирует о подключениях в консоли:

![](assets/task3server.png)

## Вывод

В результате удалось создать минимальный HTTP-сервер на TCP сокетах, который корректно отдаёт HTML-страницу по запросу клиента.
Это демонстрирует базовые принципы работы веб-серверов и взаимодействия по протоколу HTTP.