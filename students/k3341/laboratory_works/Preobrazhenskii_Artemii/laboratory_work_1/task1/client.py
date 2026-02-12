import socket


def run_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto("Hello, server".encode(), ('localhost', 8080))

    data, _ = client_socket.recvfrom(1024)
    print(data.decode())

    client_socket.close()

if __name__ == "__main__":
    run_client()