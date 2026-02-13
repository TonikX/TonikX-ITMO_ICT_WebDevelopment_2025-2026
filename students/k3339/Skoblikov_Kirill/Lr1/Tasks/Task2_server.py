import socket
from math import sqrt

def quadratic_Solution(a, b, c):
    if a == 0:
        if b == 0:
            return "Уравнение вырождено"
        return round(-c / b, 2)

    D = b ** 2 - 4 * a * c

    if D < 0:
        return "Действительных корней нет"
    elif D == 0:
        root = float(-b / (2 * a))
        return round(root, 2)
    else:
        first_root = (-b - sqrt(D)) / (2 * a)
        second_root = (-b + sqrt(D)) / (2 * a)
        return round(first_root, 2), round(second_root, 2)


# Создаем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет к адресу и порту
server_socket.bind(('localhost', 8911))

# Начинаем слушать входящие подключения (ожидание клиентов)
server_socket.listen(1)
print("Сервер запущен на порту 8911...")

while True:
    # Принимаем соединение от клиента
    client_connection, client_address = server_socket.accept()
    print(f'Подключение от {client_address}')

    client_connection.sendall('Чтобы я мог решить квадратное уравнение, передай мне коэффициенты a, b и c в формате "a, b, c"'.encode())

    # Получаем сообщение от клиента
    while True:
        try:
            data = client_connection.recv(1024).decode()
            if not data:
                print(f"Клиент {client_address} отключился")
                break

            request = list(map(float, data.split(sep=', ')))
            response = quadratic_Solution(float(request[0]), float(request[1]), float(request[2]))
            if type(response) == tuple:
                client_connection.sendall(f'Первый корень: {response[0]}, Второй: {response[1]}'.encode())
            elif type(response) == float:
                client_connection.sendall(f'Единственный корень: {response}'.encode())
            else:
                client_connection.sendall(f'Либо отсутствуют действительные корни, либо уравнение вырождено'.encode())
        except:
            client_connection.sendall(f'Некорректные входные данные'.encode())

    # Закрываем соединение
    client_connection.close()