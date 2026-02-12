import socket

from utils import get_parallelogram_area


def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    server_socket.bind(('localhost', 8080))
    print("Server running")
    server_socket.listen(1)

    while True:
        client_connection, client_address = server_socket.accept()
        request = client_connection.recv(1024).decode()
        try:
            base_str, height_str = request.split()
            base = float(base_str)
            height = float(height_str)
            client_connection.sendall(f"{get_parallelogram_area(base, height)}".encode())
        except Exception as e:
            client_connection.sendall(f"Ошибка: {e}".encode())
        client_connection.close()


if __name__ == "__main__":
    run_server()