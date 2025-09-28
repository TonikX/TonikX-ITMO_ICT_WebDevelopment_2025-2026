import socket


def solve_sqr(a, b, c):
    d = b**2 - 4*a*c
    if d < 0:
        return "корней нет"
    else:
        return f"ответ: x1 = {(-b + d**0.5)/(2*a)}, x2 = {(-b - d**0.5)/(2*a)}"


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('localhost', 8080))

server_socket.listen(1)
print("Сервер запущен на порту 8080...")

while True:
    client_connection, client_address = server_socket.accept()
    print(f'Подключение от {client_address}')

    request = list(map(int, client_connection.recv(1024).decode().split()))

    print(f'Данные от клиента: a:{request[0]} b:{request[1]} c:{request[2]}')

    response = solve_sqr(request[0], request[1], request[2])

    client_connection.sendall(response.encode())

    client_connection.close()
    print("соединение закрыто")