import socket

HOST = '127.0.0.1'
PORT = 9090

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST, PORT))

print('Программа для расчёта площади трапеции')

# Пользователь вводит параметры трапеции, необходимые для подсчёта площади
while True:
    try:
        low = input('Введите длину нижнего основания: ')
        high = input('Введите длину верхнего основания: ')
        height = input('Введите длину высоты: ')
        if all(value > 0 for value in map(float, (low, high, height))):
            break
        else:
            print('Все значения должны быть положительными!')
    except:
        print('Неверный формат! Попробуйте ещё раз.')

request = f'{low} {high} {height}'

client_socket.sendall(request.encode('utf-8'))

response = client_socket.recv(1024)

print(f'Площадь трапеции: {response.decode('utf-8')}')

client_socket.close()