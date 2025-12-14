import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 8888)
message = "Hello, server"

client_socket.sendto(message.encode('utf-8'), server_address)
print(f"Отправлено сообщение: {message}")

data, addr = client_socket.recvfrom(1024)
response = data.decode('utf-8')
print(f"Получен ответ от сервера: {response}")

client_socket.close()

