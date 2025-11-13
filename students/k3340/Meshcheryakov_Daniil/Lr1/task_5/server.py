import socket, json, os, urllib.parse
from datetime import datetime
from collections import defaultdict

HOST = "127.0.0.1"
PORT = 8081
DATA_FILE = "grades.json"

def load():
    if os.path.exists(DATA_FILE):
        return json.load(open(DATA_FILE, encoding="utf-8"))
    return []

def save(data):
    json.dump(data, open(DATA_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

def build_response(status, body):
    body_b = body.encode("utf-8")
    headers = f"HTTP/1.1 {status}\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: {len(body_b)}\r\n\r\n"
    return headers.encode() + body_b

def render(data):
    grouped = defaultdict(list)
    for d in data:
        grouped[d["subject"]].append((d["grade"], d["ts"]))

    rows = "".join(
        f"<tr><td>{i+1}</td><td>{subj}</td><td>{', '.join(g for g, _ in grades)}</td><td>{grades[-1][1]}</td></tr>"
        for i, (subj, grades) in enumerate(grouped.items())
    )

    return f"""<html><body>
<h1>Оценки по дисциплинам</h1>
<form method="POST" action="/grades">
<input name="subject" placeholder="Дисциплина">
<input name="grade" placeholder="Оценка">
<button>OK</button>
</form>
<table border=1>
<tr><th>#</th><th>Дисциплина</th><th>Оценки</th><th>Последнее обновление</th></tr>
{rows or "<tr><td colspan=4>Нет данных</td></tr>"}
</table>
</body></html>"""

def handle(conn):
    req = conn.recv(65535).decode("utf-8")
    if not req:
        return
    headers, _, body = req.partition("\r\n\r\n")
    if not headers.strip():
        return
    line = headers.splitlines()[0]
    method, path, _ = line.split()
    data = load()
    if method == "POST" and path.startswith("/grades"):
        params = urllib.parse.parse_qs(body)
        subj = params.get("subject", [""])[0]
        grade = params.get("grade", [""])[0]
        if subj and grade:
            data.append({"subject": subj, "grade": grade, "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
            save(data)
        resp = "HTTP/1.1 303 See Other\r\nLocation: /\r\n\r\n".encode()
    else:
        resp = build_response("200 OK", render(data))
    conn.sendall(resp)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"[GRADES SERVER] http://{HOST}:{PORT}")
        while True:
            conn, _ = s.accept()
            with conn:
                handle(conn)

if __name__ == "__main__":
    main()
