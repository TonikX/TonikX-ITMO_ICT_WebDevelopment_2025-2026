import socket

a = input("a: ")
b = input("b: ")
c = input("c: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9999))
client.send(f"{a} {b} {c}".encode())
result = client.recv(1024).decode()
print(f"Result: {result}")
client.close()
