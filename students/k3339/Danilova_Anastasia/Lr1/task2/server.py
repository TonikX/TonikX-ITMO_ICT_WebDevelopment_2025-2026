# server.py
# 4th option - parallelogram's area
import socket
import math

TCP_PORT = 9090
sock = socket.socket()
sock.bind(('localhost', TCP_PORT))
sock.listen(1)

greeting_msg = ('Hello! You can calculate parallelogram\'s area in two ways:'
                '\n1: by base and a height'
                '\n2: two sides and angle between them'
                '\nIf you want to start type the number of the option you need (1 or 2)')

try:
    while True:
        conn, addr = sock.accept()
        print(f'Connected: {addr}')
        try:
            conn.send(greeting_msg.encode('utf-8'))
            data = conn.recv(1024)

            if not data:
                conn.close()
                continue

            option = data.decode('utf-8')
            if option == '1':
                conn.send('\nType base:'.encode('utf-8'))
                data = conn.recv(1024)
                base = int(data.decode('utf-8'))
                conn.send('\nType height:'.encode('utf-8'))
                data = conn.recv(1024)
                height = int(data.decode('utf-8'))

                answer = str(base * height)

            elif option == '2':
                conn.send('\nType side1:'.encode('utf-8'))
                data = conn.recv(1024)
                side1 = int(data.decode('utf-8'))
                conn.send('\nType side2:'.encode('utf-8'))
                data = conn.recv(1024)
                side2 = int(data.decode('utf-8'))
                conn.send('\nType angle:'.encode('utf-8'))
                data = conn.recv(1024)
                angle = int(data.decode('utf-8'))
                angle_radians = math.radians(angle)
                answer = side1 * side2 * math.sin(angle_radians)
                answer = str(math.ceil(answer))

            else:
                answer = 'Invalid option'

            conn.send(answer.encode('utf-8'))

        except Exception as e:
            print(f'Error: {e}')
        finally:
            conn.close()
except KeyboardInterrupt:
    print('\nServer stopped')
finally:
    sock.close()
