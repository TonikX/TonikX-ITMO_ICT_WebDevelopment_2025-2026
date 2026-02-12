import os
import socket

current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, "index.html")

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    server_socket.bind(('localhost', 8080))
    print("Server running at http://localhost:8080/")
    server_socket.listen(1)

    while True:
        client_connection, _ = server_socket.accept()
        _ = client_connection.recv(1024).decode()

        with open(file_path, "rb") as f:
            html = f.read()

        response = b"HTTP/1.1 200 OK\r\n" \
                       b"Content-Type: text/html; charset=utf-8\r\n" \
                       b"Content-Length: " + str(len(html)).encode() + b"\r\n" \
                       b"\r\n" + html
        client_connection.sendall(response)
        client_connection.close()

if __name__ == "__main__":
    run_server()