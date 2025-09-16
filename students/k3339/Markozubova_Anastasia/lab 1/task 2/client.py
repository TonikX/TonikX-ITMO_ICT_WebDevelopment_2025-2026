import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 8080))
a = float(input())
b = float(input())

data = f"{a} {b}"

sock.send(data.encode())
print(sock.recv(1024).decode())
sock.close()
print("Сокет закрыт")