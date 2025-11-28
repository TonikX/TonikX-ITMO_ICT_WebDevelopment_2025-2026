import socket
import threading


def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            print(msg)
        except:
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8888))


thread = threading.Thread(target=receive_messages, args=(client_socket,))
thread.start()


while True:
    msg = input()
    if msg == '/quit':
        break
    client_socket.send(msg.encode())

client_socket.close()
