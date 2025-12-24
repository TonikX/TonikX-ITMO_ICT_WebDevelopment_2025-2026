import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(('localhost', 8080))

http_request = "GET / HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n"
client_socket.sendall(http_request.encode('utf-8'))

response = b""
while True:
    chunk = client_socket.recv(4096)
    if not chunk:
        break
    response += chunk

print(response.decode('utf-8'))

client_socket.close()