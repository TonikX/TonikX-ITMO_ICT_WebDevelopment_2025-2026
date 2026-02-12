import socket

HOST = 'localhost'
PORT = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)
print(f"Server is running on {HOST}:{PORT}")

while True:
    conn, addr = sock.accept()
    print(f"Подключен клиент: {addr}")
    try:
        request = conn.recv(1024).decode()
        print(f"Запрос:\n{request}")

        try:
            with open("index.html", "r", encoding="utf-8") as f:
                html_content = f.read()
        except FileNotFoundError:
            html_content = "<h1>Файл index.html не найден</h1>"

        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type: text/html; charset=utf-8\r\n"
        response += f"Content-Length: {len(html_content.encode('utf-8'))}\r\n"
        response += "\r\n"
        response += html_content

        conn.sendall(response.encode('utf-8'))
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        conn.close()
