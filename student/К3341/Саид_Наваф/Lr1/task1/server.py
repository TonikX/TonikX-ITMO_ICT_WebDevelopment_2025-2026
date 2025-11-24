import socket

HOST = "127.0.0.1"
PORT = 8081

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    print(f"UDP server listening on {HOST}:{PORT}")
    while True:
        data, addr = s.recvfrom(4096)
        print(f"Received from {addr}: {data.decode()}")
        s.sendto(b"Hello, client!", addr)