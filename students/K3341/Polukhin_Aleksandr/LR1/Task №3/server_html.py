import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('localhost', 8080))

server_socket.listen(1)

while True:
    client_connection, client_address = server_socket.accept()

    request = client_connection.recv(1024).decode()

    with open('index.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(html_content.encode('utf-8'))}\r\n"
        "Connection: close\r\n"
        "\r\n" +
        html_content
    )

    client_connection.sendall(response.encode('utf-8'))

    client_connection.close()