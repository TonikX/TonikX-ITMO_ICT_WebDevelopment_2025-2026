import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('localhost', 8888))

print("Сервер запущен на порту 8888")

while True:
    data, addr = server_socket.recvfrom(1024)
    message = data.decode('utf-8')
    print(f"Получено сообщение от {addr}: {message}")
    
    response = "Hello, client"
    server_socket.sendto(response.encode('utf-8'), addr)
    print(f"Отправлен ответ: {response}")

