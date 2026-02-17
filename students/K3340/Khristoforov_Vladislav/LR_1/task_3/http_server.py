import socket
import os

HOST = 'localhost'
PORT = 12345
BUFFER_SIZE = 1024

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(script_dir, "index.html")
    
    if not os.path.exists(html_path):
        print(f"Ошибка: файл {html_path} не найден")
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        
        print(f"Сервер запущен на {HOST}:{PORT}")
        
        try:
            while True:
                conn, addr = s.accept()
                
                with conn:
                    conn.recv(BUFFER_SIZE)
                    
                    with open(html_path, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    
                    response = (
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: text/html; charset=utf-8\r\n"
                        f"Content-Length: {len(html_content.encode('utf-8'))}\r\n"
                        "\r\n"
                        f"{html_content}"
                    )
                    
                    conn.sendall(response.encode('utf-8'))
                    
                    print(f"Отправлена страница клиенту {addr[0]}")
                    
        except KeyboardInterrupt:
            print("\nСервер остановлен")

if __name__ == "__main__":
    main()