import socket
import math

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('localhost', 8080))

server_socket.listen(1)

while True:
    client_connection, client_address = server_socket.accept()

    data = client_connection.recv(1024).decode()

    a_str, b_str, c_str = data.split(',')
    a, b, c = float(a_str), float(b_str), float(c_str)

    D = b**2 - 4*a*c
    if D > 0:
        x1 = (-b + math.sqrt(D)) / (2*a)
        x2 = (-b - math.sqrt(D)) / (2*a)
        result = f"Два корня: x1 = {x1}, x2 = {x2}"
    elif D == 0:
        x = -b / (2*a)
        result = f"Один корень: x = {x}"
    else:
        result = "Действительных корней нет"

    client_connection.sendall(result.encode())

    client_connection.close()