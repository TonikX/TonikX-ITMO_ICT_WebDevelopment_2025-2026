import socket
from urllib.parse import parse_qs, unquote_plus

grades = {}

with open("index.html", "r") as f:
    HTML_TEMPLATE = f.read()

def build_table():
    if not grades:
        return '<div class="empty">No grades yet</div>'
    rows = "".join(f"<tr><td>{s}</td><td>{g}</td></tr>" for s, g in grades.items())
    return f"<table><tr><th>Subject</th><th>Grade</th></tr>{rows}</table>"

def handle(conn):
    raw = conn.recv(4096).decode()
    if not raw:
        conn.close()
        return
    first_line = raw.split("\r\n")[0]
    method = first_line.split(" ")[0]
    if method == "POST":
        body = raw.split("\r\n\r\n", 1)[1]
        params = parse_qs(body)
        subject = unquote_plus(params.get("subject", [""])[0])
        grade = unquote_plus(params.get("grade", [""])[0])
        if subject and grade:
            grades[subject] = grade
    page = HTML_TEMPLATE.replace("{{content}}", build_table())
    response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: {len(page.encode())}\r\n\r\n{page}"
    conn.sendall(response.encode())
    conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("localhost", 9999))
server.listen(5)
print("Server is running on http://localhost:9999")
while True:
    conn, _ = server.accept()
    handle(conn)
