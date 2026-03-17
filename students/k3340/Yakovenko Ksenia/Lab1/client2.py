import socket

HOST = "127.0.0.1"
PORT = 30114

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

a = input("Enter base a: ")
b = input("Enter base b: ")
h = input("Enter height h: ")

message = f"{a} {b} {h}"
client_socket.sendall(message.encode())

data = client_socket.recv(1996).decode()
print("Answer from server:", data)

client_socket.close()
