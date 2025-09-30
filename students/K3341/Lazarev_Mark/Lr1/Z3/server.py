import socket

HOST = "127.0.0.1"
PORT = 8080

# Загружаем содержимое HTML-файла
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Формируем HTTP-ответ
http_response = f"""\
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: {len(html.encode("utf-8"))}

{html}
"""

# Создаём TCP-сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Сервер запущен на http://{HOST}:{PORT}/")

while True:
    conn, addr = server_socket.accept()
    request = conn.recv(1024).decode()
    print(f"\nЗапрос от {addr}:\n{request}")
    conn.sendall(http_response.encode("utf-8"))
    conn.close()
