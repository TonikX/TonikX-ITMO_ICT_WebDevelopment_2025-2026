import socket

HOST = '127.0.0.1'
PORT = 9090


def main():
    # Создаём сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Отправляем сообщения
    message = 'Hello, server'
    client_socket.sendto(message.encode('utf-8'), (HOST, PORT))

    # Получаем ответа
    try:
        server_data, server_address = client_socket.recvfrom(1024)
        print(f"Ответ от сервера: {server_data.decode('utf-8')}")
    except:
        print("Сервер недоступен.")

    # Закрываем сокет
    client_socket.close()


if __name__ == '__main__':
    main()
