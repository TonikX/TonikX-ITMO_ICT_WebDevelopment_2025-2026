import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('localhost', 8080))

server_socket.listen(1)
print("Сервер запущен на порту 8080...")


def is_valid_trapezoid(a, b, h):
    if a <= 0 or b <= 0 or h <= 0:
        return False
    return True


while True:
    client_connection, client_address = server_socket.accept()
    print(f'Подключение от {client_address}')

    request = client_connection.recv(1024).decode()
    print(f'Запрос от клиента: {request}')

    try:
        a, b, h = list(map(float, request.split(':')))

        if is_valid_trapezoid(a, b, h):
            S = (a + b) / 2 * h
            response = f'Площадь трапеции - {S}'
        else:
            response = 'Ошибка: Введенные значения не могут образовать трапецию'
    except Exception as e:
        response = f'Ошибка при обработке данных: {str(e)}'

    client_connection.sendall(response.encode())
    client_connection.close()
