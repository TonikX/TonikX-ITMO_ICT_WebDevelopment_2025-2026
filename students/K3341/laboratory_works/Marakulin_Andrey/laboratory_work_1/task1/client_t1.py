import socket
from utils import server_address


def start_client(address: tuple):
    """Создает UDP сокет клиента и отправляет сообщение серверу с адресом address"""
    # Создаем UDP сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    message = 'Hello, server'
    # Отправляем сообщение серверу
    sent = client_socket.sendto(message.encode('utf-8'), address)

    # Ждем ответа от сервера
    server_data, server = client_socket.recvfrom(1024)
    # Декодируем полученные байты обратно в строку
    print(f'Получен ответ: ', server_data.decode("utf-8"))

    client_socket.close()


if __name__ == "__main__":
    start_client(server_address)
