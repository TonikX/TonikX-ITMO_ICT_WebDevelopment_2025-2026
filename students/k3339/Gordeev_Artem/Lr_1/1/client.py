import socket

# AF_INET - IPv4, SOCK_DGRAM - UDP
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr = ('localhost', 9999)
message = "Hello, server"

udp_socket.sendto(message.encode('utf-8'), addr)
print(f"Отправил: '{message}'")

data, server = udp_socket.recvfrom(1024)

print(f"Получил ответ: '{data.decode('utf-8')}'")