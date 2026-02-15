import socket

HOST = '127.0.0.1'
PORT = 9090

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen(1)

print(f'Сервер запущен на {HOST}:{PORT}')

while True:
    client_connection, client_address = server_socket.accept()
    print(f'Подключение. {client_address}')

    try:
        # HTML
        with open('index.html', 'rb') as html_file:
            html_content = html_file.read()

        # Header
        headers = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(html_content)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        ).encode('utf-8')

        client_connection.sendall(headers + html_content)

    except:
        print('Ошибка ответа')

    client_connection.close()
