import socket
from math import sin, radians
from config import HOST, PORT

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.bind((HOST, PORT))
conn.listen(10)
while True:
    try:
        client_socket, addr = conn.accept()
        print(type(addr), addr)
        data = client_socket.recv(16384).decode()
        print("получен запрос:", data)

        a, b, angle = map(float, data.split(", "))
        angle = radians(angle)
        s = round(a * b * sin(angle), 2)

        client_socket.send(str(s).encode())
        client_socket.close()

    except KeyboardInterrupt:
        conn.close()
        break
