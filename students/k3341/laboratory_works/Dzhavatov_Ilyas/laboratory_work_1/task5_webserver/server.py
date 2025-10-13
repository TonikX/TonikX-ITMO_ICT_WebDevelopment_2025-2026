import socket
import urllib.parse
from collections import defaultdict

HOST = "127.0.0.1"
PORT = 8081


grades = defaultdict(list)


def build_html():
    """Подставляем таблицу с оценками в index.html"""
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            template = f.read()
    except FileNotFoundError:
        return "<h1>index.html not found</h1>"

    if grades:
        rows = []
        for subject, grade_list in grades.items():

            grades_str = ", ".join(grade_list)
            rows.append(f"<tr><td>{subject}</td><td>{grades_str}</td></tr>")

        table = f"<table border='1'><tr><th>Дисциплина</th><th>Оценки</th></tr>{''.join(rows)}</table>"
    else:
        table = "<p>Пока нет оценок</p>"

    return template.replace("{grades_table}", table)


def handle_request(request: str) -> str:
    """Обработка HTTP-запроса"""
    headers = request.split("\r\n")
    if not headers:
        return "HTTP/1.1 400 Bad Request\r\n\r\n"

    first_line = headers[0]
    method, path, _ = first_line.split(" ")

    if method == "GET":
        body = build_html()
        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type: text/html; charset=utf-8\r\n"
        response += f"Content-Length: {len(body.encode('utf-8'))}\r\n"
        response += "Connection: close\r\n"
        response += "\r\n"
        response += body
        return response

    elif method == "POST":

        parts = request.split("\r\n\r\n", 1)
        if len(parts) < 2:
            return "HTTP/1.1 400 Bad Request\r\n\r\n"
        body_data = parts[1]


        form = urllib.parse.parse_qs(body_data)
        subject = form.get("subject", [""])[0].strip()
        grade = form.get("grade", [""])[0].strip()

        if subject and grade:

            grades[subject].append(grade)


        body = build_html()
        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type: text/html; charset=utf-8\r\n"
        response += f"Content-Length: {len(body.encode('utf-8'))}\r\n"
        response += "Connection: close\r\n"
        response += "\r\n"
        response += body
        return response

    else:
        return "HTTP/1.1 405 Method Not Allowed\r\n\r\n"


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print(f"Server running on http://{HOST}:{PORT}")

    try:
        while True:
            conn, addr = server_socket.accept()
            request = conn.recv(4096).decode("utf-8", errors="ignore")
            print(f"\nClient {addr}:\n{request}\n")

            response = handle_request(request)
            conn.sendall(response.encode("utf-8"))
            conn.close()
    except KeyboardInterrupt:
        print("Server stopped")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
