import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((socket.gethostname(), 1234))

client.send('Hello, server'.encode('utf-8'))
print(client.recv(1024).decode('utf-8'))
client.send('Bye, server'.encode('utf-8'))
print(client.recv(1024).decode('utf-8'))
