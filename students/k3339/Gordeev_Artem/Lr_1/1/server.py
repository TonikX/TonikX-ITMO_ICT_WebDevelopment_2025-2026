import socket

# AF_INET - IPv4, SOCK_DGRAM - UDP
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

udp_socket.bind(('localhost', 9999))
message = "Hello, client"

while True:
    print("Ожидание...")
    data, addr = udp_socket.recvfrom(1024)
    print(f"Получено сообщение от {addr}: {data.decode('utf-8')}")

    udp_socket.sendto(message.encode('utf-8'), addr)
    print(f"Ответ отправлен")