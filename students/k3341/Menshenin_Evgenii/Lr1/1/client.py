import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client_socket.sendto(b'Hello, server!', ("localhost", 8081))

response, address = client_socket.recvfrom(1024)
print(response.decode())
