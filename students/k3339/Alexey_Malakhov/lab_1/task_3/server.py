import socket

HOST = 'localhost'
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen(5)
print(f"HTTP сервер запущен на {HOST}:{PORT}...")

while True:
    client_connection, client_address = server_socket.accept()
    print(f'Подключение от {client_address}')

    with open('index.html', 'r') as f:
        html_content = f.read()
    html_bytes = html_content.encode('utf-8')

    request = client_connection.recv(1024).decode()
    print(f'Запрос клиента:\n{request}')

    http_response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=UTF-8\r\n"
        f"Content-Length: {len(html_bytes)}\r\n"
        "Connection: close\r\n"
        "\r\n" + html_content
    )

    client_connection.sendall(http_response.encode())

    client_connection.close()
