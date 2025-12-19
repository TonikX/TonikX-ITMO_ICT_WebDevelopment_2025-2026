import socket
from threading import Thread

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(('localhost', 777))

name_request = client_socket.recv(1024).decode()
print(name_request, end='')

name = input()
client_socket.send(name.encode("utf-8"))


def receive_messages():
    while True:
        try:
            server_message = client_socket.recv(1024).decode()
            if server_message:
                print(server_message)
            else:
                break
        except Exception as e:
            print(e)
            break


def send_messages():
    while True:
        message = input()

        if message.lower() == 'выход':
            break
        client_socket.send(message.encode("utf-8"))


receive_thread = Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()

send_messages()

client_socket.close()
