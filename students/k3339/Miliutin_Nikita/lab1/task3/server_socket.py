import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 9090))

server_socket.listen(1)

connection_socket, addr = server_socket.accept()
with connection_socket as conn:
    with open("index.html", "rb") as f:
        html_bytes = f.read()
        headers = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(html_bytes)}\r\n"
        "\r\n"
            ).encode('utf-8')

        conn.sendall(headers + html_bytes)

