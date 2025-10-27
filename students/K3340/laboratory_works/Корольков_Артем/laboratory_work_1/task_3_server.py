import socket
import os


def load_html_file(filename):
    """Загружает содержимое HTML-файла"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "<html><body><h1>404 - File Not Found</h1></body></html>"


def main():
    # Создаем TCP-сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Привязываем сокет к адресу и порту
    server_address = ('localhost', 8080)
    server_socket.bind(server_address)

    # Начинаем прослушивание входящих подключений
    server_socket.listen(5)
    print(f"HTTP-сервер запущен на http://{server_address[0]}:{server_address[1]}")

    while True:
        try:
            # Принимаем подключение
            client_socket, client_address = server_socket.accept()
            print(f"Подключился клиент: {client_address}")

            # Получаем HTTP-запрос
            request = client_socket.recv(1024).decode('utf-8')
            print(f"Получен запрос:\n{request}")

            # Загружаем HTML-страницу из файла
            html_content = load_html_file('index.html')

            # Формируем HTTP-ответ
            response_headers = [
                'HTTP/1.1 200 OK',
                'Content-Type: text/html; charset=utf-8',
                f'Content-Length: {len(html_content)}',
                'Connection: close',
                '\r\n'
            ]

            # Объединяем заголовки и содержимое
            response = '\r\n'.join(response_headers) + html_content

            # Отправляем ответ клиенту
            client_socket.sendall(response.encode('utf-8'))
            print("Отправлен HTTP-ответ с содержимым index.html")

            # Закрываем соединение с клиентом
            client_socket.close()

        except KeyboardInterrupt:
            print("\nСервер остановлен")
            break
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            if 'client_socket' in locals():
                client_socket.close()


if __name__ == "__main__":
    main()