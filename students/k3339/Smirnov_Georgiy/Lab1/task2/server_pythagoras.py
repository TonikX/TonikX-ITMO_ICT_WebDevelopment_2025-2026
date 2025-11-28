import socket

def pythagoras(a, b):
    return (a ** 2 + b ** 2) ** 0.5

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 9000))
server_socket.listen()
print('Сервер по теореме Пифагора запущен...')

while True:
    client_socket, addr = server_socket.accept()
    print('Клиент подключился:', addr)
    data = client_socket.recv(1024).decode()
    try:
        a, b = map(float, data.strip().split())
        result = pythagoras(a, b)
        answer = f'Гипотенуза для катетов {a} и {b}: {result:.3f}'
    except Exception:
        answer = 'Ошибка! Введите два числа через пробел'
    client_socket.send(answer.encode())
    client_socket.close()
