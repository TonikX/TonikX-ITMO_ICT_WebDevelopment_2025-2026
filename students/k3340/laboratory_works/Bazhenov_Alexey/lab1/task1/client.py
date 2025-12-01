import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 8080)
message = 'Hello, server!'
client_socket.sendto(message.encode(), server_address)

response, server_addr = client_socket.recvfrom(1024)
print(f'Ответ от сервера {server_addr}: {response.decode()}')

