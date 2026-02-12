import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

PORT = 8080

sock.bind(('', PORT))

print("[UDP] Server is running on port {}".format(PORT))

while True:
    data, addr = sock.recvfrom(1024)
    print(f"Получено от {addr}: {data.decode()}")

    sock.sendto(b'Hello, client', addr)
