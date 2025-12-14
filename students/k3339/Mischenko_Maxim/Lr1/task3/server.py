import socket

with open('index.html', 'r') as f:
    html_content = f.read()

with socket.socket() as server_socket:
    host = 'localhost'
    port = 8080

    server_socket.bind((host, port))
    print(f'socket bound to {host}:{port}')

    server_socket.listen(5)
    while True:
        client_connection, client_address = server_socket.accept()
        with client_connection:
            print('Connected by', client_address)

            request = client_connection.recv(1024).decode()
            print(f'request: {request}')

            html_response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html\r\n"
                f"Content-Length: {len(html_content)}\r\n"
                "Connection: close\r\n"
                "\r\n"
                + html_content
            )

            client_connection.sendall(html_response.encode())

            client_connection.close()
