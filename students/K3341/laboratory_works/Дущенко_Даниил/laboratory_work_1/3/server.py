import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 8080))
sock.listen(1)

while True:
    conn, addr = sock.accept()
    request = conn.recv(1024)
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + content
    conn.sendall(response.encode('utf-8'))
    conn.close()