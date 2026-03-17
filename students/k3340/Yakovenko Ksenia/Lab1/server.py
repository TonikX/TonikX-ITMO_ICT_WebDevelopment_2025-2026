import socket

HOST = "127.0.0.1"   # local adr
PORT = 30114         # port

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

print(f"UDP server is launched on {HOST}:{PORT}")

while True:
    data, addr = sock.recvfrom(1996)
    print(f"Received from {addr}: {data.decode()}")

    if data:
        response = "Hello, client"
        sock.sendto(response.encode(), addr)  # answer sending