import socket

while True:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        user_input = str(input())
        client_socket.connect(('localhost', 8082))
        client_socket.sendall(user_input.encode())
        response = client_socket.recv(1024)
        print(response.decode())
    except Exception as e:
        print(f"wrong input: {e}")
        continue

    client_socket.close()
