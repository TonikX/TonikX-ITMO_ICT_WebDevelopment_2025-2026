# client.py
import socket

UDP_IP = '127.0.0.1'
UDP_PORT = 9090
sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
addr = (UDP_IP, UDP_PORT)
message = 'Hello, server!'
sock.sendto(message.encode('utf-8'), addr)

data, server = sock.recvfrom(1024)
print(data.decode('utf-8'))
sock.close()