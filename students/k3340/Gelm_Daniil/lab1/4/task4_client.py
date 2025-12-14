import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            print(data.decode('utf-8'))
        except:
            break

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8891))

recv_thread = threading.Thread(target=receive_messages, args=(client_socket,))
recv_thread.daemon = True
recv_thread.start()

print("Подключен к чату. Введите сообщение:")

while True:
    message = input()
    if message == '/quit':
        break
    client_socket.send(message.encode('utf-8'))

client_socket.close()

