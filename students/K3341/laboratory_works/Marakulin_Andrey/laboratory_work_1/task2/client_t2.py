import socket
from utils import server_address


def start_client(address: tuple):
    """Создает TCP сокет клиента и отправляет данные с катетами серверу с адресом address"""
    # Создаем TCP сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect(address)

    a_str = input('Введите первый катет (a): ')
    b_str = input('Введите второй катет (b): ')
    message = f'{a_str},{b_str}'

    # Отправляем данные
    client_socket.sendall(message.encode('utf-8'))

    # Получаем ответ
    data = client_socket.recv(1024)
    print(f'Ответ сервера (гипотенуза): {data.decode("utf-8")}')

    client_socket.close()


if __name__ == "__main__":
    start_client(server_address)
