import socket

HOST = '127.0.0.1'
PORT = 8080 

def run_server_http():
    
    try:
        with open('index3.html', 'r', encoding='utf-8') as f:
            HTML_CONTENT = f.read()
    except FileNotFoundError:
        print("❌ Ошибка: Файл 'index.html' не найден!")
        return


    HTTP_HEADERS = (
        "HTTP/1.1 200 OK\r\n" 
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(HTML_CONTENT.encode('utf-8'))}\r\n"
        "Connection: close\r\n" 
        "\r\n" 
    )
    FULL_RESPONSE = (HTTP_HEADERS + HTML_CONTENT).encode('utf-8')
    
    # Настройка и запуск TCP-сокета
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Позволяет повторно использовать адрес (полезно при частых перезапусках)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"HTTP Сервер (Задание 3) запущен на http://{HOST}:{PORT}")
        print("Ожидание подключений...")
        
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"\nПодключен клиент: {addr}")
                
                request_data = conn.recv(1024)
                if not request_data:
                    continue
                    
                conn.sendall(FULL_RESPONSE)
                print("Ответ (index.html) отправлен.")

if __name__ == '__main__':
    run_server_http()