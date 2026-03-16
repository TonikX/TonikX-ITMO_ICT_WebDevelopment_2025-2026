import socket

HOST = "127.0.0.1"
PORT = 8080

request = "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    client_socket.sendall(request.encode())
    response = client_socket.recv(4096).decode()
    print("Ответ сервера:\n")
    print(response)
