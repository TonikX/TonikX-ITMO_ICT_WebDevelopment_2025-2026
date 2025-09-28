import socket

SERVER_ADDRESS = ("127.0.0.1", 10000)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Установка соединения с сервером
        client_socket.connect(SERVER_ADDRESS)

        # Отправка сообщения серверу
        message = input()
        client_socket.sendall(message.encode("utf-8"))

        # Получение сообщения от сервера
        data = client_socket.recv(1024)
        print(data.decode("utf-8", errors="replace"))

if __name__ == "__main__":
    main()

