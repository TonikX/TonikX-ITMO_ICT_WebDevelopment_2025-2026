import socket

HOST = "127.0.0.1"
PORT = 8001

with open("index.html", "rb") as f:
    html = f.read()

response = b"HTTP/1.1 200 OK\r\n" + \
           b"Content-Type: text/html; charset=utf-8\r\n" + \
           b"Content-Length: " + str(len(html)).encode() + b"\r\n\r\n" + html

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"Static server on http://{HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        with conn:
            conn.sendall(response)