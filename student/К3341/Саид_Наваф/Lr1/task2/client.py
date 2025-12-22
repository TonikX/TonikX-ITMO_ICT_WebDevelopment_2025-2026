import socket

HOST = "127.0.0.1"
PORT = 8082

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        message = input("Enter three numbers a,b,h (or 'quit'): ")
        if message.lower() == 'quit':
            break
        s.sendall(message.encode())
        data = s.recv(4096)
        print(f"Result: {data.decode()}")