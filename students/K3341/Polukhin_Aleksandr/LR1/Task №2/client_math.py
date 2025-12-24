import socket

a = input("Введите коэффициент a: ")
b = input("Введите коэффициент b: ")
c = input("Введите коэффициент c: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(('localhost', 8080))

message = f"{a},{b},{c}"
client_socket.sendall(message.encode())

response = client_socket.recv(1024)
print(f"Ответ от сервера: {response.decode()}")

client_socket.close()