import socket

SERVER_ADDRESS = ("127.0.0.1", 10000)

def main():
    # socket.SOCK_DGRAM указывает, что это UDP-сокет
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind(SERVER_ADDRESS)

        while True:
            # Получение данных от клиента
            data, addr = server_socket.recvfrom(1024)
            print(data.decode("utf-8", errors="replace"))

            # Отправка данных клиенту
            message = "Hello, client"
            server_socket.sendto(message.encode("utf-8"), addr)

if __name__ == "__main__":
    main()