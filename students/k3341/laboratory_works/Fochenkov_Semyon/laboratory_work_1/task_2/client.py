import socket

HOST = "127.0.0.1"
PORT = 12345

print("Решение квадратного уравнения вида ax^2 + bx + c = 0")

while True:
    a = input("Введите a (или q для выхода): ")
    if a == "q":
        break
    b = input("Введите b: ")
    c = input("Введите c: ")

    request = f"{a} {b} {c}"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        client_socket.sendall(request.encode())

        data = client_socket.recv(1024).decode()
        print("Результат:", data)
