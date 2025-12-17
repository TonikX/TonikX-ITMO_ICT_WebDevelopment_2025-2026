import socket
from utils import server_address


def start_server(address):
    """Создает веб-сервер на адресе address, который при подключении клиента, отправляет ему HTTP-сообщение,
    содержащие HTML-страницу index.html"""

    # Создаем сокет
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(address)
    sock.listen(1)
    print(f'Сервер запущен на http://{address[0]}:{address[1]}')

    while True:
        connection, client_address = sock.accept()
        try:
            # Принимаем запрос от браузера
            request = connection.recv(1024)
            print(f"Получен запрос:\n{request.decode('utf-8')}")

            # Читаем содержимое файла
            with open('index.html', 'r', encoding='utf-8') as f:
                html_content = f.read()

            # Формируем HTTP-ответ
            response = (
                'HTTP/1.1 200 OK\r\n'
                'Content-Type: text/html; charset=utf-8\r\n'
                f'Content-Length: {len(html_content.encode("utf-8"))}\r\n'
                '\r\n'
                f'{html_content}'
            )
            connection.sendall(response.encode('utf-8'))

        finally:
            connection.close()


if __name__ == "__main__":
    start_server(server_address)
