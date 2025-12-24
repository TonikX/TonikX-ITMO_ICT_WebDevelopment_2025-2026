import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_socket.bind(('localhost', 8080))

print('Сервер запущен и ждёт сообщений...')

while True:
    # Получаем данные и адрес клиента
    data, client_address = server_socket.recvfrom(1024)
    print(f'От клиента ({client_address}): {data.decode()}')

    # Отправляем ответ
    response = 'Hello, client'
    server_socket.sendto(response.encode(), client_address)
