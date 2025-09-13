import socket
from utils import server_address


def start_server(address):
    """Создает UDP сокет сервера на адресе address, принимает сообщение от клиента и отправляет ему приветственное сообщение"""
    # Создаем UDP сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(address)
    print(f'Сервер запущен на {address[0]}:{address[1]}')

    while True:
        # Получаем данные от клиента
        client_data, client_address = server_socket.recvfrom(1024)
        if client_data:
            print("Получены данные: ", client_data.decode("utf-8"))
            # Отправляем ответ обратно клиенту
            response = 'Hello, client'
            sent = server_socket.sendto(response.encode('utf-8'), client_address)


if __name__ == "__main__":
    start_server(server_address)
