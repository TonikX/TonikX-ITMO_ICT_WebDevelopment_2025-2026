import socket

HOST = "127.0.0.1"
PORT = 30114

# TCP-server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"TCP server is launched on {HOST}:{PORT}, waiting for connection...")

while True:
    conn, addr = server_socket.accept()
    print(f"Client is connected: {addr}")

    data = conn.recv(1996).decode()
    print(f"Received: {data}")

    try:
        a, b, h = map(float, data.split())
        result = (a + b) / 2 * h
        response = f"Trapezoid square = {result}"
    except Exception as e:
        response = f"Error: {e}"

    conn.sendall(response.encode())
    conn.close()
