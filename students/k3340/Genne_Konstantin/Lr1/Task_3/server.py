import socket

HOST = '127.0.0.1'
PORT = 9090

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen(1)

print(f'Сервер запущен на {HOST}:{PORT}')


while True:
    client_connection, client_address = server_socket.accept()

    with open('index.html', 'r', encoding='UTF-8') as html_file:
        html_content = html_file.read()

    content_length = len(html_content.encode('utf-8'))

    http_response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=UTF-8\r\n"
        f"Content-Length: {content_length}\r\n"
        "Connection: close\r\n"
        "\r\n"
        + html_content
    )

    client_connection.sendall(http_response.encode('UTF-8'))

    client_connection.close()
      