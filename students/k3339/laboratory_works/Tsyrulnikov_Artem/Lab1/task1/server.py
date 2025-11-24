import socket


class Config:
    HOST = "0.0.0.0"
    PORT = 8001
    BUFFER_SIZE = 1024


def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((Config.HOST, Config.PORT))
    print(f"Сервер запущен на {Config.HOST}:{Config.PORT}")

    while True:
        data, client_address = server_socket.recvfrom(Config.BUFFER_SIZE)

        message: str = data.decode("utf-8")
        print(f"{client_address[0]}:{client_address[1]} -> {message}")
        response = "Hello, client"

        server_socket.sendto(response.encode("utf-8"), client_address)
        print(f"{client_address[0]}:{client_address[1]} <- {response}")


if __name__ == "__main__":
    run_server()
