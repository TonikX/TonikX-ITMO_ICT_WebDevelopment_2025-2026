import socket
from utils import server_address
from math_utils import *


def start_server(address: tuple):
    """Создает TCP сокет сервера на адресе address, принимает данные о катетах от клиента, считает гипотенузу
    по теореме Пифагора и отправляет клиенту результат"""

    # Создаем TCP сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(address)
    print(f'Сервер запущен на {address[0]}:{address[1]}')

    server_socket.listen(1)

    while True:
        # Получаем данные от клиента
        connection, client_address = server_socket.accept()

        # Получаем данные
        data = connection.recv(1024)

        if data:
            # Декодируем данные и разбираем их
            decoded_data = data.decode('utf-8')
            print(f'Получены данные: {decoded_data}')
            try:
                parts = decoded_data.split(',')
                a = float(parts[0])
                b = float(parts[1])

                # Вычисляем результат
                result = calculate_pythagoras(a, b)
                response = str(result)
            except (ValueError, IndexError):
                response = 'Ошибка: неверный формат данных. Ожидается (float, float)'

            # Отправляем результат клиенту
            connection.sendall(response.encode('utf-8'))

            # Закрываем соединение с клиентом
            connection.close()


if __name__ == "__main__":
    start_server(server_address)
