import socket

with open("index.html", "rb") as f:
    html = f.read()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    host = 'localhost'
    port = 8001

    s.bind((host, port))
    s.listen()

    while True:
        con, addr = s.accept()
        with con:
            con.sendall(html)
