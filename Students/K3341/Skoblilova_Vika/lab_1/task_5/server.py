import socket
import threading
from urllib.parse import parse_qs

grades = {}

def generate_html():
    html = """
    <html>
    <head>
        <meta charset="utf-8">
        <title>Оценки</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f5f5f5;
                margin: 0;
                padding: 0;
            }
            .container {
                max-width: 600px;
                margin: 50px auto;
                background: #fff;
                padding: 20px 30px;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }
            h1, h2 { text-align: center; color: #333; }
            ul { list-style: none; padding: 0; }
            li {
                background: #e9f0ff;
                margin: 6px 0;
                padding: 10px 14px;
                border-radius: 8px;
                font-size: 16px;
            }
            form { margin-top: 20px; display: flex; flex-direction: column; gap: 10px; }
            input[type="text"] {
                padding: 10px;
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 8px;
            }
            input[type="submit"] {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                font-size: 14px;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                transition: 0.2s;
            }
            input[type="submit"]:hover { background-color: #45a049; }
            p { text-align: center; color: #777; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Список оценок</h1>
    """

    if grades:
        html += "<ul>"
        for subject, grade in grades.items():
            html += f"<li><b>{subject}</b>: {grade}</li>"
        html += "</ul>"
    else:
        html += "<p>Пока нет оценок.</p>"

    html += """
            <h2>Добавить оценку</h2>
            <form method="POST">
                <input type="text" name="subject" placeholder="Дисциплина">
                <input type="text" name="grade" placeholder="Оценка">
                <input type="submit" value="Сохранить">
            </form>
        </div>
    </body>
    </html>
    """
    return html

def handle_request(request_data):
    try:
        headers, body = request_data.split("\r\n\r\n", 1)
    except ValueError:
        headers, body = request_data, ""

    lines = headers.split("\r\n")
    method, path, _ = lines[0].split()

    if method == "POST":
        data = parse_qs(body)
        subject = data.get("subject", [""])[0].strip()
        grade = data.get("grade", [""])[0].strip()
        if subject and grade:
            grades[subject] = grade

    response_body = generate_html()
    response = "HTTP/1.1 200 OK\r\n"
    response += "Content-Type: text/html; charset=utf-8\r\n"
    response += f"Content-Length: {len(response_body.encode('utf-8'))}\r\n"
    response += "\r\n"
    response += response_body
    return response

def handle_client(client_socket, addr):
    try:
        request = client_socket.recv(1024).decode("utf-8", errors="ignore")
        if not request:
            client_socket.close()
            return

        headers = request.split("\r\n\r\n", 1)[0]
        content_length = 0
        for line in headers.split("\r\n"):
            if line.lower().startswith("content-length:"):
                content_length = int(line.split(":")[1].strip())

        body = request.split("\r\n\r\n", 1)[1] if "\r\n\r\n" in request else ""
        body_bytes = body.encode("utf-8")
        while len(body_bytes) < content_length:
            body_bytes += client_socket.recv(1024)
        full_request = headers + "\r\n\r\n" + body_bytes.decode("utf-8", errors="ignore")

        response = handle_request(full_request)
        client_socket.sendall(response.encode("utf-8"))
    finally:
        client_socket.close()

def run_server():
    host = "127.0.0.1"
    port = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Многопоточный сервер запущен на http://{host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Подключился клиент {addr}")
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    run_server()
