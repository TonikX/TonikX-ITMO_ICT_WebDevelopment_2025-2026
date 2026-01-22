# server.py
import socket

UDP_IP = '127.0.0.1'
UDP_PORT = 9090
sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))
sock.settimeout(1.0) # тайм аут для операций блокирующих сокет

response = 'Hello, client!'

try:
    while True:
        try:
            data, addr = sock.recvfrom(1024)
        except socket.timeout:
            continue
        if not data:
            break
        print(data.decode('utf-8'))
        sock.sendto(response.encode('utf-8'), addr)
except KeyboardInterrupt:
    print('\nserver stopped')
finally:
    sock.close()

