import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('localhost', 1234))
server_socket.listen(1)


while True:
    client_socket, address = server_socket.accept()

    data = client_socket.recv(1024).decode()
    print("request:\n", data)
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            html = f.read()

        http_response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=UTF-8\r\n"
            f"Content-Length: {len(html.encode('utf-8'))}\r\n"
            "Connection: close\r\n"
            "\r\n"
            f"{html}"
        )

    except:
        http_response = (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            "Connection: close\r\n"
            "\r\n"
            "<h1>404 — file index.html not found</h1>"
        )
    client_socket.sendall(http_response.encode())
    client_socket.close()


