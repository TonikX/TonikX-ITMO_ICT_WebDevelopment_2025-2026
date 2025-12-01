import socket

HOST = '127.0.0.1'
PORT = 9090

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

while True:
    print("\nВведите стороны и высоту трапеции (a b h), или 'e' для выхода:")
    msg = input("> ")
    if msg.lower() == 'e':
        break

    client_socket.send(msg.encode())
    data = client_socket.recv(1024).decode()
    print("Ответ сервера:", data)

client_socket.close()