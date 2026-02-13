import socket
import urllib.parse
from collections import defaultdict

grades = []


def build_html():
    grouped = defaultdict(list)
    for d, g in grades:
        grouped[d].append(g)

    rows = ""
    for discipline, marks in grouped.items():
        marks_str = ", ".join(marks)
        rows += f"<tr><td>{discipline}</td><td>{marks_str}</td></tr>"

    html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>Оценки по дисциплинам</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f0f2f5;
                height: 100vh;
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            .container {{
                background-color: white;
                border-radius: 16px;
                padding: 30px 40px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                width: 450px;
                text-align: center;
            }}
            h1 {{
                margin-bottom: 20px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }}
            th, td {{
                border: 1px solid #ccc;
                padding: 8px;
            }}
            th {{
                background-color: #f7f7f7;
            }}
            input[type="text"] {{
                width: 90%;
                padding: 6px;
                margin: 5px 0;
                border: 1px solid #ccc;
                border-radius: 6px;
            }}
            input[type="submit"] {{
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 18px;
                border-radius: 6px;
                cursor: pointer;
                margin-top: 10px;
            }}
            input[type="submit"]:hover {{
                background-color: #45a049;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Список оценок</h1>
            <table>
                <tr><th>Дисциплина</th><th>Оценки</th></tr>
                {rows if rows else "<tr><td colspan='2'>Нет данных</td></tr>"}
            </table>

            <h2>Добавить новую оценку</h2>
            <form method="POST" action="/">
                <input type="text" name="discipline" placeholder="Дисциплина" required><br>
                <input type="text" name="grade" placeholder="Оценка" required><br>
                <input type="submit" value="Добавить">
            </form>
        </div>
    </body>
    </html>
    """
    return html


def read_http_request(conn):
    data = b""
    while b"\r\n\r\n" not in data:
        part = conn.recv(1024)
        if not part:
            break
        data += part

    header_part, _, body = data.partition(b"\r\n\r\n")
    headers = header_part.decode("utf-8", errors="ignore")

    content_length = 0
    for line in headers.split("\r\n"):
        if line.lower().startswith("content-length:"):
            try:
                content_length = int(line.split(":")[1].strip())
            except ValueError:
                content_length = 0
            break

    while len(body) < content_length:
        part = conn.recv(1024)
        if not part:
            break
        body += part

    full_request = header_part + b"\r\n\r\n" + body
    return full_request.decode("utf-8", errors="ignore")


def handle_request(request):
    headers, _, body = request.partition("\r\n\r\n")
    if not headers:
        return "HTTP/1.1 400 Bad Request\r\n\r\n"

    first_line = headers.split("\r\n")[0]
    try:
        method, path, _ = first_line.split()
    except ValueError:
        return "HTTP/1.1 400 Bad Request\r\n\r\n"

    if method == "POST":
        decoded_body = urllib.parse.unquote_plus(body)
        params = urllib.parse.parse_qs(decoded_body)
        discipline = params.get("discipline", [""])[0]
        grade = params.get("grade", [""])[0]

        if discipline and grade:
            grades.append((discipline, grade))

        return "HTTP/1.1 303 See Other\r\nLocation: /\r\n\r\n"

    html = build_html()
    return "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n" + html


def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('127.0.0.1', 8911))
        s.listen(5)
        print(f"Сервер запущен: http://{'127.0.0.1'}:{8911}/")

        while True:
            conn, addr = s.accept()
            with conn:
                request = read_http_request(conn)
                if not request:
                    continue
                response = handle_request(request)
                conn.sendall(response.encode("utf-8"))


if __name__ == "__main__":
    run_server()