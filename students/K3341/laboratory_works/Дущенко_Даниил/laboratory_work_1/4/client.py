import socket
import threading

def receive(sock):
    while True:
        try:
            data = sock.recv(1024)
            print(data.decode('utf-8'))
        except:
            break

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 5555))

threading.Thread(target=receive, args=(sock,)).start()

name = input("Name: ")
while True:
    msg = input()
    sock.send(f"{name}: {msg}".encode('utf-8'))