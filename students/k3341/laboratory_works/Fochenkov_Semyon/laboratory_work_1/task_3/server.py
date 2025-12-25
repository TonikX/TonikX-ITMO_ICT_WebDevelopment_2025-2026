import socket
import threading

HOST = "127.0.0.1"
PORT = 8080


def handle_client(conn, addr):
    print(f"[+] Подключен клиент {addr}")
    try:
        request = conn.recv(1024).decode()
        print("Запрос:\n", request)

        try:
            with open("index.html", "r", encoding="utf-8") as f:
                body = f.read()
        except FileNotFoundError:
            body = "<h1>404 Not Found</h1>"

        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(body.encode('utf-8'))}\r\n"
            "\r\n"
            f"{body}"
        )
        conn.sendall(response.encode("utf-8"))
    except Exception as e:
        print("Ошибка:", e)
    finally:
        conn.close()
        print(f"[-] Клиент {addr} отключился")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"HTTP-сервер запущен: http://{HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
        thread.start()
