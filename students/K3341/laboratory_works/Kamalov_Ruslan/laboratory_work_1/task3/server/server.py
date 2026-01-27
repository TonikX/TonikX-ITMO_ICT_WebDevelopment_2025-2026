import socket
from cfg import SERVER_HOST, SERVER_PORT, BUFFER_SIZE, HTML_FILE

def load_html():
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        return f.read()

def create_http_response(html_content):
    body = html_content.encode('utf-8')
    
    headers = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body)}\r\n"
        "Connection: close\r\n"
        "\r\n"
    )
    return headers.encode('utf-8') + body

def start_http_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    
    print(f"[*] HTTP Сервер запущен на http://{SERVER_HOST}:{SERVER_PORT}")
    print("[*] Откройте адрес в браузере")
    print("[*] Для остановки нажмите Ctrl+C")
    
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"\n[+] Подключение от {client_address}")
            
            request = client_socket.recv(BUFFER_SIZE).decode('utf-8')
            
            if request:
                request_line = request.split('\n')[0]
                print(f"[+] Запрос: {request_line.strip()}")
                
                html_content = load_html()
                response = create_http_response(html_content)
                
                client_socket.send(response)
                print(f"[+] Ответ отправлен ({len(html_content)} байт)")
            
            client_socket.close()
            
    except KeyboardInterrupt:
        print("\n[!] Сервер остановлен пользователем")
    finally:
        server_socket.close()
        print("[*] Сокет закрыт")

if __name__ == "__main__":
    start_http_server()
