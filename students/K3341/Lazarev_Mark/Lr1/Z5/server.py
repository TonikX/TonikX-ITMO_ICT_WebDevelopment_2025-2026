import socket
from urllib.parse import parse_qs

HOST = "127.0.0.1"
PORT = 8080

# Хранилище оценок (в памяти, пока сервер работает)
grades = []

def build_html():
    """Генерация HTML-страницы со всеми оценками"""
    rows = "".join(f"<tr><td>{subj}</td><td>{grade}</td></tr>" for subj, grade in grades)
    return f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Оценки</title>
    </head>
    <body>
        <h1>Список оценок</h1>
        <form method="POST" action="/">
            Дисциплина: <input type="text" name="subject">
            Оценка: <input type="text" name="grade">
            <button type="submit">Добавить</button>
        </form>
        <h2>Таблица</h2>
        <table border="1" cellpadding="5">
            <tr><th>Дисциплина</th><th>Оценка</th></tr>
            {rows}
        </table>
    </body>
    </html>
    """

def make_response(html: str):
    """Собираем HTTP-ответ"""
    body = html.encode("utf-8")
    headers = (
        "HTTP/1.1 200 OK\r\n"
        f"Content-Length: {len(body)}\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        "Connection: close\r\n"
        "\r\n"
    )
    return headers.encode("utf-8") + body

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f"Сервер запущен: http://{HOST}:{PORT}/")

    while True:
        conn, addr = server_socket.accept()
        request = conn.recv(4096).decode("utf-8", errors="ignore")
        if not request:
            conn.close()
            continue

        headers, _, body = request.partition("\r\n\r\n")
        request_line = headers.split("\n")[0]
        method, path, _ = request_line.split()

        if method == "POST":

            params = parse_qs(body)
            subject = params.get("subject", [""])[0].strip()
            grade = params.get("grade", [""])[0].strip()
            if subject and grade:
                grades.append((subject, grade))

        response = make_response(build_html())
        conn.sendall(response)
        conn.close()

if __name__ == "__main__":
    main()
