import socket

HOST = '127.0.0.1'
PORT = 9090

def trapezoid_area(low, high, height):
    """
    Функция предназначена для подсчёта площади трапеции.
    Параметры:
        low - длина нижнего основания
        high - длина верхнего основания
        height - высота
    """
    return (low + high) / 2 * height


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen(1)

print(f'Сервер запущен на {HOST}:{PORT}')

while True:
    client_connection, client_address = server_socket.accept()

    request = client_connection.recv(1024).decode()

    response = trapezoid_area(*map(float, request.split()))

    client_connection.sendall(str(response).encode())

    client_connection.close()