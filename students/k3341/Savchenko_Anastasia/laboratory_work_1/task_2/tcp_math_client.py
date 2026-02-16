import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 1235))

base = float(input("Основание: "))
height = float(input("Высота: "))

client.send(f"{base} {height}".encode())
result = client.recv(1024).decode()
print("Площадь:", result)

client.close()