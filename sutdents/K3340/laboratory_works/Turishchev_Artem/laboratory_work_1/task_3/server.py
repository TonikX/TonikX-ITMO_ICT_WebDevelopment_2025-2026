import socket
from config import HOST, PORT

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.bind((HOST, PORT))
conn.listen(10)

while True:
    try:
        client_socket, addr = conn.accept()
        data = client_socket.recv(16384).decode()
        print("получен запрос:", data)

        response_type = "HTTP/1.1 200 OK\r\n"
        headers = "Content-Type: text/html; charset=utf-8\r\n\r\n"
        with open("index.html", encoding="utf-8") as file:
            body = file.read()
        msg = response_type + headers + body
        client_socket.send(msg.encode())
        client_socket.close()

    except KeyboardInterrupt:
        conn.close()
        break
