import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
msg = input("Введите сообщение для сервера: ")
client_socket.sendto(msg.encode(), ('localhost', 8080))
data, _ = client_socket.recvfrom(1024)
print('Ответ от сервера:', data.decode())
client_socket.close()
