import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("localhost", 9999))
server.listen(1)
print("Server is running on http://localhost:9999")
while True:
    conn, addr = server.accept()
    conn.recv(1024)
    with open("index.html", "r") as f:
        body = f.read()
    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(body)}\r\n\r\n{body}"
    conn.sendall(response.encode())
    conn.close()
