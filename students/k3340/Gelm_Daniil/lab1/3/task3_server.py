import socket

def load_html(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return "<html><body><h1>Ошибка загрузки файла</h1></body></html>"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8890))
server_socket.listen(5)

print("HTTP сервер запущен на порту 8890")

html_content = load_html('index.html')

while True:
    client_socket, addr = server_socket.accept()
    print(f"Подключен клиент: {addr}")
    
    request = client_socket.recv(1024).decode('utf-8')
    
    response = f"HTTP/1.1 200 OK\r\n"
    response += f"Content-Type: text/html; charset=utf-8\r\n"
    response += f"Content-Length: {len(html_content.encode('utf-8'))}\r\n"
    response += f"\r\n"
    response += html_content
    
    client_socket.send(response.encode('utf-8'))
    client_socket.close()

