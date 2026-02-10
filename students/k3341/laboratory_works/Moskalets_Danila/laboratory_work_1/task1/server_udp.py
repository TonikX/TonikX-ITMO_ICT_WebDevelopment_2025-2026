import socket

HOST = '127.0.0.1'
PORT = 9090

# создаем udp сокет: af_inet - ipv4, sock_dgram - udp
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# привязываем сокет к адресу
server_socket.bind((HOST, PORT))
print(f"UDP сервер запущен на {HOST}:{PORT}")

while True:
    # получаем сообщение от клиента
    data, addr = server_socket.recvfrom(1024)
    message = data.decode('utf-8')
    print(f"Получено сообщение от {addr}: {message}")

    # отправляем ответ клиенту
    response = "Hello, client"
    server_socket.sendto(response.encode('utf-8'), addr)