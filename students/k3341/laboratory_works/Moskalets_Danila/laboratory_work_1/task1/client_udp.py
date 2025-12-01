import socket

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9090

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# отправляем сообщение серверу
message = "Hello, server"
client_socket.sendto(message.encode('utf-8'), (SERVER_HOST, SERVER_PORT))

# получаем ответ от сервера
data, _ = client_socket.recvfrom(1024)
print("Ответ от сервера:", data.decode('utf-8'))

client_socket.close()