import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 8080))

print("1-Pythagoras, 2-Quadratic, 3-Trapezoid, 4-Parallelogram")
op = input("Operation: ")
params = input("Params: ")

sock.send(f"{op} {params}".encode('utf-8'))
data = sock.recv(1024)
print(f"Result: {data.decode('utf-8')}")
sock.close()