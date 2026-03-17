import socket
import urllib.parse

HOST = "127.0.0.1"
PORT = 30117

# использую словарь
grades = {}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print(f"Server is running: http://{HOST}:{PORT}")

def build_page():
    rows = ""
    for subj, marks in grades.items():
        rows += f"<tr><td>{subj}</td><td>{', '.join(marks)}</td></tr>"
    return f"""
    <html><body>
        <h1>Marks</h1>
        <table border="1" cellpadding="5">
            <tr><th>Subject</th><th>Marks</th></tr>
            {rows}
        </table>
        <form method="POST">
            <p>Subject: <input name="subject"></p>
            <p>Mark: <input name="mark"></p>
            <p><input type="submit" value="Add"></p>
        </form>
    </body></html>
    """

while True:
    conn, addr = server.accept()
    request = conn.recv(2002).decode()

    headers, _, body = request.partition("\r\n\r\n")
    if request.startswith("POST"):
        params = urllib.parse.parse_qs(body)
        subj = params.get("subject", [""])[0]
        mark = params.get("mark", [""])[0]
        if subj and mark:
            grades.setdefault(subj, []).append(mark)

    page = build_page()
    response = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n" + page
    conn.sendall(response.encode())
    conn.close()
