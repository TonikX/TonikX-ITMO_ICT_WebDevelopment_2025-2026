import socket
import mimetypes

HOST = 'localhost'
PORT = 9093


def get_file_content(filename):
    try:
        with open(filename, 'rb') as file:
            return file.read()
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Ошибка чтения файла {filename}: {e}")
        return None


def get_content_type(filename):
    """Определение MIME-типа файла"""
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type if mime_type else 'text/plain'

def create_http_response(status_code, content_type, content):
    """Создание HTTP-ответа"""
    status_messages = {
        200: "OK",
        404: "Not Found",
        500: "Internal Server Error"
    }

    status_line = f"HTTP/1.1 {status_code} {status_messages.get(status_code, 'Unknown')}"
    headers = [
        f"Content-Type: {content_type}; charset=UTF-8",
        f"Content-Length: {len(content)}",
        "Connection: close",
        "Server: Python-HTTP-Server/1.0"
    ]

    response = f"{status_line}\r\n"
    response += "\r\n".join(headers)
    response += "\r\n\r\n"

    return response.encode('utf-8') + content


def handle_request(request_data):
    """Обработка HTTP-запроса"""
    try:
        lines = request_data.decode('utf-8').split('\n')
        if not lines:
            return create_http_response(400, 'text/plain', b'Bad Request')

        request_line = lines[0].strip()
        parts = request_line.split()

        if len(parts) < 2:
            return create_http_response(400, 'text/plain', b'Bad Request')

        method = parts[0]
        path = parts[1]

        print(f"Запрос: {method} {path}")

        # Обрабатываем только GET запросы
        if method != 'GET':
            return create_http_response(405, 'text/plain', b'Method Not Allowed')

        # По умолчанию отдаем index.html
        if path == '/' or path == '/index.html':
            filename = 'index.html'
        else:
            filename = path.lstrip('/')

        # Читаем содержимое файла
        content = get_file_content(filename)

        if content is None:
            # Файл не найден
            error_content = """
            <html>
            <head><title>404 Not Found</title></head>
            <body>
                <h1>404 - Страница не найдена</h1>
                <p>Запрашиваемый файл не найден на сервере.</p>
                <a href="/">Вернуться на главную</a>
            </body>
            </html>
            """.encode('utf-8')
            return create_http_response(404, 'text/html', error_content)

        # Определяем MIME-тип
        content_type = get_content_type(filename)

        # Создаем успешный ответ
        return create_http_response(200, content_type, content)

    except Exception as e:
        print(f"Ошибка обработки запроса: {e}")
        error_content = """
        <html>
        <head><title>500 Internal Server Error</title></head>
        <body>
            <h1>500 - Внутренняя ошибка сервера</h1>
            <p>Произошла ошибка при обработке запроса.</p>
        </body>
        </html>
        """.encode('utf-8')
        return create_http_response(500, 'text/html', error_content)


def main():
    """Основная функция сервера"""
    # Создаем TCP сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Позволяем повторно использовать адрес
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        # Привязываем сокет к адресу и порту
        server_socket.bind((HOST, PORT))

        # Начинаем слушать входящие соединения
        server_socket.listen(5)
        print(f"HTTP сервер запущен на {HOST}:{PORT}")
        print("Откройте браузер и перейдите по адресу: http://localhost:9093")
        print("Для остановки сервера нажмите Ctrl+C")

        while True:
            # Принимаем соединение от клиента
            client_connection, client_address = server_socket.accept()
            print(f'Подключение от {client_address}')

            try:
                # Получаем HTTP-запрос
                request_data = client_connection.recv(4096)

                if request_data:
                    # Обрабатываем запрос и получаем ответ
                    response = handle_request(request_data)

                    # Отправляем ответ клиенту
                    client_connection.sendall(response)
                    print(f'Ответ отправлен клиенту {client_address}')

            except Exception as e:
                print(f"Ошибка при обработке клиента {client_address}: {e}")
            finally:
                # Закрываем соединение
                client_connection.close()

    except KeyboardInterrupt:
        print("\nСервер остановлен пользователем")
    except Exception as e:
        print(f"Ошибка сервера: {e}")
    finally:
        # Закрываем сокет
        server_socket.close()
        print("Сервер завершил работу")


if __name__ == "__main__":
    main()
