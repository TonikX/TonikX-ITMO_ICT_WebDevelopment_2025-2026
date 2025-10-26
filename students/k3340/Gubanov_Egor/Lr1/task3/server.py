import socket
import threading
import os

HOST = '127.0.0.1'
PORT = 8003
INDEX_FILE = 'index.html'
ENCODING = 'utf-8'

def create_http_response(status_code, body):
    status_text = {
        200: "200 OK",
        404: "404 Not Found"
    }.get(status_code, "500 Internal Server Error")
    
    headers = [
        f"HTTP/1.1 {status_text}",
        f"Content-Type: text/html; charset=utf-8",
        f"Content-Length: {len(body)}",
        "Connection: close",
        "",
        ""
    ]
    return "\r\n".join(headers).encode(ENCODING) + body

def handle_client(conn, addr):
    with conn:
        try:
            data = conn.recv(1024).decode(ENCODING)
            if not data:
                return

            first_line = data.splitlines()[0]
            parts = first_line.split()
            if len(parts) < 3:
                return
                
            method, path, version = parts
            print(f"Запрос: {method} {path} от {addr}")

            if method == 'GET' and path == '/':
                if os.path.exists(INDEX_FILE):
                    with open(INDEX_FILE, 'r', encoding=ENCODING) as f:
                        html_content = f.read()
                    response = create_http_response(200, html_content.encode(ENCODING))
                else:
                    error_html = "<html><body><h1>404 Not Found</h1><p>Файл index.html не найден</p></body></html>"
                    response = create_http_response(404, error_html.encode(ENCODING))
            else:
                error_html = "<html><body><h1>404 Not Found</h1><p>Страница не найдена</p></body></html>"
                response = create_http_response(404, error_html.encode(ENCODING))
            
            conn.sendall(response)
                
        except Exception as e:
            print(f"Ошибка: {e}")

def main():
    print("🌐 HTTP Сервер")
    print("=" * 20)
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        
        print(f"✅ Сервер запущен на http://{HOST}:{PORT}/")
        print(f"📁 Файл: {INDEX_FILE}")
        print("\nНажмите Ctrl+C для остановки...")
        
        try:
            while True:
                conn, addr = s.accept()
                thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
                thread.start()
        except KeyboardInterrupt:
            print("\n🛑 Сервер остановлен")

if __name__ == '__main__':
    main()
