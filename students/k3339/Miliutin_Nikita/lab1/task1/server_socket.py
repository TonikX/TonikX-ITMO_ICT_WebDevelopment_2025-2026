import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("localhost", 9090))

print("Сервереный сокет запущен! (вывел сервер)")


while True:
    data, addr = server_socket.recvfrom(1024)
    print("Подключение с адреса: ", addr, " (вывел сервер)")
    client_request = data.decode()
    print(client_request, " (вывел сервер)")
    server_response = "Привет от сервера!"
    server_socket.sendto(server_response.encode(), addr)
    print("Ответ отправлен (вывеел сервер)")
