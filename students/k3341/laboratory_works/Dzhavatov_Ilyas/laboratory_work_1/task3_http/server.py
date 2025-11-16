# server.py
import socket

HOST = '127.0.0.1'   # локальный хост
PORT = 8080          # порт (можно поменять, если занят)

def main():
    # читаем HTML из файла
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    # готовим HTTP-ответ
    response = "HTTP/1.1 200 OK\r\n"
    response += "Content-Type: text/html; charset=utf-8\r\n"
    response += f"Content-Length: {len(html_content.encode('utf-8'))}\r\n"
    response += "Connection: close\r\n"
    response += "\r\n"  # пустая строка отделяет заголовки от тела
    response += html_content

    # создаём TCP-сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    print(f"HTTP server running on http://{HOST}:{PORT}")

    try:
        while True:
            conn, addr = server_socket.accept()
            print(f"Client connected: {addr}")

            # читаем запрос (нам не важно его содержимое)
            request = conn.recv(1024).decode("utf-8")
            print(f"Request:\n{request}\n")

            # отправляем ответ
            conn.sendall(response.encode("utf-8"))
            conn.close()
    except KeyboardInterrupt:
        print("Server stopped")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
