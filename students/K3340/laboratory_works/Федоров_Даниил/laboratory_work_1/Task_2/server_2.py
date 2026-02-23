import socket
import math

def equation(a, b, c):
    try:
        a, b, c = float(a), float(b), float(c)
        if a == 0:
            return 'Коэффициент A не может быть равен нулю'

        discr = b ** 2 - 4 * a * c

        if discr > 0:
            x1 = (-b + math.sqrt(discr)) / (2 * a)
            x2 = (-b - math.sqrt(discr)) / (2 * a)
            return f'Ответ: X1 = {x1}, X2 = {x2}'
        elif discr == 0:
            x = -b / (2 * a)
            return f'Ответ: X = {x}'
        else:
            return 'Корней нет'

    except ValueError:
        return 'Введены некорректные числа'




server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 1234))

server_socket.listen(1)
print('Сервер запущен')

while True:
    client_socket, address = server_socket.accept()
    print('Клиент подключился')


    data = client_socket.recv(1024).decode().split()
    if len(data) == 3:
        a, b, c = data
        client_socket.sendall(equation(a,b, c).encode())
    else:
        client_socket.sendall('Вы ввели не 3 значения'.encode())

    client_socket.close()



