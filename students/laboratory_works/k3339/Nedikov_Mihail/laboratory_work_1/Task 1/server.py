import socket

# UDP-сервер принимает сообщения от клиентов и отвечает фиксированной строкой.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Привязываем сокет к адресу localhost:8080.
server_socket.bind(("localhost", 8080))

while True:
    # Ждём сообщение от клиента и выводим его тело.
    request, address = server_socket.recvfrom(1024)
    print(request.decode())

    # Отправляем ответ тому же клиенту.
    response = "Hello, client"
    server_socket.sendto(response.encode(), address)
