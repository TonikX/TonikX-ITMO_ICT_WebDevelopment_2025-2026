import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 8080))
sock.listen()
conn, addr = sock.accept()

request = conn.recv(2048).decode()

with open("index.html", "rb") as f:
    html_bytes = f.read()
    lenght = len(html_bytes)
    headers = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {lenght}\r\n"
        "Connection: close\r\n"
        "\r\n"
    )
    conn.sendall(headers.encode("utf-8"))
    conn.sendall(html_bytes)
    conn.close()
sock.close()



