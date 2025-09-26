import socket
import math

# TCP-сервер принимает соединение, читает два числа и считает гипотенузу.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет и переводим его в режим прослушивания.
server_socket.bind(("localhost", 8080))
server_socket.listen(1)

while True:
    # Ждём клиента и считываем строку с числами.
    client_connection, client_address = server_socket.accept()
    request = client_connection.recv(1024).decode()

    try:
        numbers = list(map(float, request.split()))
        if len(numbers) != 2:
            raise ValueError("Нужно ввести ровно два числа.")
        if any(n < 0 for n in numbers):
            raise ValueError("Числа должны быть неотрицательными.")
        result = str(math.sqrt(numbers[0] ** 2 + numbers[1] ** 2))
    except ValueError as error:
        result = f"Ошибка: {error}"

    # Отправляем ответ клиенту и закрываем соединение.
    client_connection.sendall(result.encode())
    client_connection.close()
