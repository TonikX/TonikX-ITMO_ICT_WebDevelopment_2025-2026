# client.py
import socket

TCP_IP = 'localhost'
TCP_PORT = 9090
sock = socket.socket()
sock.connect((TCP_IP, TCP_PORT))

data = sock.recv(1024)
print(data.decode('utf-8'))

option = input()
sock.send(option.encode('utf-8'))

if option == '1':
    data = sock.recv(1024)
    print(data.decode('utf-8'))
    base = input()
    sock.send(base.encode('utf-8'))

    data = sock.recv(1024)
    print(data.decode('utf-8'))
    height = input()
    sock.send(height.encode('utf-8'))

elif option == '2':
    data = sock.recv(1024)
    print(data.decode('utf-8'))
    side1 = input()
    sock.send(side1.encode('utf-8'))

    data = sock.recv(1024)
    print(data.decode('utf-8'))
    side2 = input()
    sock.send(side2.encode('utf-8'))

    data = sock.recv(1024)
    print(data.decode('utf-8'))
    angle = input()
    sock.send(angle.encode('utf-8'))

result = sock.recv(1024).decode('utf-8')
print(f'Result: {result}')
sock.close()
