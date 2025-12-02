import socket


def run_server(server_host: str = 'localhost', server_port: int = 8080):
    '''
    Простой TCP-сервер, который отправляет HTML-страницу по запросу от клиента
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((server_host, server_port))
        server.listen(1)
        print(f'Сервер запущен на {server_host}:{server_port}')

        conn, addr = server.accept()

        with conn:
            print(f'Подключён клиент {addr}')

            # читаем запрос от клиента
            data = conn.recv(1024)
            print(f'Получены данные от клиента: {data}')

            # загрузка HTML страницы
            try:
                with open('./index.html', encoding='utf-8') as html_page:
                    html_data = html_page.read()

                html_bytes = html_data.encode('utf-8')
                content_length = len(html_bytes)

                # собираем HTTP-ответ с HTML-контентом
                http_response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/html; charset=UTF-8\r\n"
                    f"Content-Length: {content_length}\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                )

                # отправляем клиенту HTML страничку
                conn.sendall(http_response.encode() + html_bytes)

            except FileNotFoundError:
                error_message = "<html><body><h1>404 Not Found</h1><p>Файл не найден</p></body></html>"

                error_bytes = error_message.encode('utf-8')
                content_length = len(error_bytes)

                http_response = (
                    "HTTP/1.1 404 Not Found\r\n"
                    "Content-Type: text/html; charset=UTF-8\r\n"
                    f"Content-Length: {content_length}\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                )

                conn.sendall(http_response.encode('utf-8') + error_bytes)


if __name__ == "__main__":
    run_server()
