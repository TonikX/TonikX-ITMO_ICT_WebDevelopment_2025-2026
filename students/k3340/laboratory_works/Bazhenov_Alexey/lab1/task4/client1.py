import socket
import threading


def process_recieve(client_socket):
    while True:
        response = client_socket.recv(1024).decode()
        print(response)


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(('localhost', 8080))

name = input("Введите имя: ")

t = threading.Thread(target=process_recieve, args=(client_socket,))
t.start()

print("вы присоединились к чату!")

while True:
    text = input()
    client_socket.sendall((name + ": " + text).encode())

