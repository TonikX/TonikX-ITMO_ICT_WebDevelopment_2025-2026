import socket

HOST = 'localhost'
PORT = 8080

def http_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"HTTP сервер запущен на http://{HOST}:{PORT}")

    while True:
        try:
            client_connection, client_address = server_socket.accept()
            print(f'Подключение от {client_address}')

            with open(r'C:\Users\Александр\itmo course\TonikX-ITMO_ICT_WebDevelopment_2025-2026\students\K3339\laboratory_works\Subbotin_Alexander\laboratory_work_1\task3\index.html', 'r', encoding="utf-8") as f:
                html_content = f.read()
            html_bytes = html_content.encode('utf-8')

            request = client_connection.recv(1024).decode('utf-8')
            print(f'Запрос клиента:\n{request}')

            http_response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=UTF-8\r\n"
                f"Content-Length: {len(html_bytes)}\r\n"
                "Connection: close\r\n"
                "\r\n" + html_content
            )

            client_connection.sendall(http_response.encode('utf-8'))
            client_connection.close()
            
        except KeyboardInterrupt:
            print("\nСервер остановлен")
            server_socket.close()
            break
        except Exception as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    http_server()