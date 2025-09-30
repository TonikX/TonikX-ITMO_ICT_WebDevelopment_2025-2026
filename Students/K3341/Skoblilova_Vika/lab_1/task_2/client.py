import socket

HOST = "127.0.0.1"
PORT = 5006

a = input("Введите основание параллелограмма: ")
h = input("Введите высоту параллелограмма: ")

message = f"{a} {h}"

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
client_socket.send(message.encode())

data = client_socket.recv(1024).decode()
print("Ответ от сервера:", data)

client_socket.close()
