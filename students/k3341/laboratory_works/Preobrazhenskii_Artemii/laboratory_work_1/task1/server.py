import socket


def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', 8080))
    print("Server running")

    while True:
        client_connection, client_address = server_socket.recvfrom(1024)
        request = client_connection.decode()

        print(request)
        server_socket.sendto(b'Hello, client', client_address)

if __name__ == "__main__":
    run_server()