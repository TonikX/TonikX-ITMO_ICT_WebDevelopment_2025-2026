import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8889))

print("Введите два катета для теоремы Пифагора:")
a = float(input("Катет a: "))
b = float(input("Катет b: "))

data = f"{a},{b}"
client_socket.send(data.encode('utf-8'))

result = client_socket.recv(1024).decode('utf-8')
print(f"Гипотенуза: {result}")

client_socket.close()

