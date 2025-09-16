import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 8080))
sock.listen()
conn, addr = sock.accept()

nums = conn.recv(1024).decode()
arr = nums.split()

a = float(arr[0])
b = float(arr[1])

c = (a ** 2 + b ** 2) ** (0.5)

answer = str(c)

conn.send(answer.encode())
sock.close()