import socket
import threading

HOST = "127.0.0.1"
PORT = 8080

def handle_client(conn, addr):
    print(f"Подключился {addr}")
    request = conn.recv(1024).decode()
    print("Запрос:\n", request)

    try:
        with open("index.html", "r", encoding="utf-8") as f:
            body = f.read()
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(body.encode('utf-8'))}\r\n"
            "Connection: close\r\n"
            "\r\n"
            f"{body}"
        )
    except FileNotFoundError:
        response = "HTTP/1.1 404 Not Found\r\n\r\n<h1>404 Not Found</h1>"

    conn.sendall(response.encode("utf-8"))
    conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"HTTP сервер запущен на http://{HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
