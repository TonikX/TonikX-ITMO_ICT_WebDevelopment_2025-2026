import socket

HOST = 'localhost'
PORT = 8080

base = float(input("Основание параллелограмма: "))
height = float(input("Высота параллелограмма: "))

params = [base, height]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
message = ','.join(map(str, params))
sock.send(message.encode())
data = sock.recv(1024)
sock.close()

print("Площадь параллелограмма:", data.decode())
