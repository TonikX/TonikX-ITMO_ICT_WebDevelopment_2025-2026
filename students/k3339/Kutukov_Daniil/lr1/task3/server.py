import socket

HOST = "127.0.0.1"
PORT = 8000

with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

http_response = f"""
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: {len(html_content.encode("utf-8"))}

{html_content}
"""

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Сервер запущен на http://{HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        with conn:
            request = conn.recv(1024).decode("utf-8")
            print("Запрос клиента:\n", request)

            # Отправляем ответ
            conn.sendall(http_response.encode("utf-8"))
