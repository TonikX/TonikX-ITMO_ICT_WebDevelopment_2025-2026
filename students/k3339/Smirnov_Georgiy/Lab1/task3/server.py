import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8081))
server.listen()
print('HTTP-сервер запущен...' \
'http://localhost:8081')

while True:
    client, addr = server.accept()
    request = client.recv(1024).decode()
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    http_response = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n" + html_content
    client.send(http_response.encode())
    client.close()
