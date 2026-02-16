import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((socket.gethostname(), 1234))

s.listen()

while True:
    client, address = s.accept()
    print(f"Connection from {address} has been established!")
    print(client.recv(1024).decode('utf-8')) # buffer for tcp
    client.send('Hello, client'.encode('utf-8'))
    print(client.recv(1024).decode('utf-8')) # buffer for tcp
    client.send('Buy!'.encode('utf-8'))

    client.close()
