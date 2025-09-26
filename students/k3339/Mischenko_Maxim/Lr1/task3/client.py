import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    host = 'localhost'
    port = 8080

    client_socket.connect((host, port))
    print(f'Connected to {host}:{port}')

    client_socket.sendall(b'52')
    print(client_socket.recv(1024).decode())
