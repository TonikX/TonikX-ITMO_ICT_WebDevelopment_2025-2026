import socket
from pathlib import Path
import urllib.parse
import json

HOST = "127.0.0.1"
PORT = 8081

DATA_PATH = Path(__file__).with_name("journal.json")

def load_journal() -> dict:
    if not DATA_PATH.exists():
        return {}
    try:
        return json.loads(DATA_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}

def save_journal(journal: dict) -> None:
    DATA_PATH.write_text(json.dumps(journal, ensure_ascii=False, indent=2), encoding="utf-8")

def http_response(body: str, status: str = "200 OK", content_type: str = "text/html; charset=utf-8") -> bytes:
    body_bytes = body.encode("utf-8")
    headers = [
        f"HTTP/1.1 {status}",
        f"Content-Type: {content_type}",
        f"Content-Length: {len(body_bytes)}",
        "Connection: close",
        "",
        ""
    ]
    return ("\r\n".join(headers)).encode("utf-8") + body_bytes

def parse_http_request(conn: socket.socket) -> tuple:
    data = b""
    while b"\r\n\r\n" not in data:
        chunk = conn.recv(4096)
        if not chunk:
            break
        data += chunk

    header_part, _, rest = data.partition(b"\r\n\r\n")
    header_text = header_part.decode("utf-8", errors="ignore")
    lines = header_text.split("\r\n")

    if not lines or len(lines[0].split()) < 2:
        return "", "", {}, b""

    request_line = lines[0]
    method, path = request_line.split()[0], request_line.split()[1]

    headers = {}
    for line in lines[1:]:
        if ":" in line:
            k, v = line.split(":", 1)
            headers[k.strip().lower()] = v.strip()

    body = rest
    if method.upper() == "POST":
        content_length = int(headers.get("content-length", "0"))
        while len(body) < content_length:
            chunk = conn.recv(4096)
            if not chunk:
                break
            body += chunk
        body = body[:content_length]

    return method.upper(), path, headers, body

def render_page(journal: dict) -> str:
    """Современный дизайн с карточками и градиентами"""
    cards = ""
    for subject, grades in journal.items():
        grades_list = [str(g) for g in grades]
        grades_str = ", ".join(grades_list)
        avg = sum(grades) / len(grades) if grades else 0
        cards += f"""
        <div class="subject-card">
            <div class="subject-header">{subject}</div>
            <div class="grades-container">
                <span class="grades-label">Оценки:</span>
                <span class="grades-list">{grades_str}</span>
            </div>
            <div class="stats">
                <div class="stat-item">
                    <span class="stat-label">Всего оценок:</span>
                    <span class="stat-value">{len(grades)}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Средний балл:</span>
                    <span class="stat-value">{avg:.2f}</span>
                </div>
            </div>
        </div>
        """

    if not cards:
        cards = '<div class="empty-state">📝 Пока нет оценок. Добавьте первую!</div>'

    return f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8" />
  <title>📚 Электронный журнал</title>
  <style>
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    body {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        padding: 20px;
    }}
    .container {{
        max-width: 1200px;
        margin: 0 auto;
    }}
    .header {{
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 30px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }}
    h1 {{
        color: #333;
        font-size: 2.5em;
        margin-bottom: 20px;
        border-left: 5px solid #667eea;
        padding-left: 20px;
    }}
    .form-container {{
        background: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
    }}
    h2 {{
        color: #555;
        margin-bottom: 20px;
        font-size: 1.5em;
    }}
    .form-group {{
        margin-bottom: 15px;
    }}
    label {{
        display: block;
        margin-bottom: 5px;
        color: #666;
        font-weight: 500;
    }}
    input {{
        width: 100%;
        padding: 10px;
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        font-size: 16px;
        transition: border-color 0.3s;
    }}
    input:focus {{
        outline: none;
        border-color: #667eea;
    }}
    button {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 8px;
        font-size: 16px;
        cursor: pointer;
        transition: transform 0.2s;
    }}
    button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }}
    .subjects-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 20px;
        margin-top: 30px;
    }}
    .subject-card {{
        background: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }}
    .subject-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }}
    .subject-header {{
        font-size: 1.3em;
        font-weight: bold;
        color: #333;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 2px solid #667eea;
    }}
    .grades-container {{
        margin-bottom: 15px;
    }}
    .grades-label {{
        color: #666;
        font-weight: 500;
    }}
    .grades-list {{
        color: #333;
        font-weight: bold;
    }}
    .stats {{
        display: flex;
        justify-content: space-between;
        background: #f8f9fa;
        padding: 10px;
        border-radius: 8px;
        margin-top: 10px;
    }}
    .stat-item {{
        text-align: center;
    }}
    .stat-label {{
        display: block;
        font-size: 0.8em;
        color: #888;
    }}
    .stat-value {{
        font-size: 1.2em;
        font-weight: bold;
        color: #667eea;
    }}
    .empty-state {{
        grid-column: 1 / -1;
        text-align: center;
        padding: 50px;
        background: white;
        border-radius: 15px;
        font-size: 1.2em;
        color: #888;
    }}
    .footer {{
        text-align: center;
        margin-top: 30px;
        color: rgba(255,255,255,0.8);
        font-size: 0.9em;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>📋 Электронный журнал успеваемости</h1>
      
      <div class="form-container">
        <h2>➕ Добавить новую оценку</h2>
        <form method="POST" action="/">
          <div class="form-group">
            <label>Название дисциплины:</label>
            <input name="subject" placeholder="Например: Математика" required>
          </div>
          <div class="form-group">
            <label>Оценка (1-5):</label>
            <input name="grade" type="number" min="1" max="5" placeholder="5" required>
          </div>
          <button type="submit">💾 Сохранить оценку</button>
        </form>
      </div>
    </div>

    <h2 style="color: white;">📊 Текущие оценки</h2>
    <div class="subjects-grid">
      {cards}
    </div>
    
    <div class="footer">
      Данные хранятся в файле journal.json | Обновлено: {__import__('datetime').datetime.now().strftime('%d.%m.%Y %H:%M')}
    </div>
  </div>
</body>
</html>
"""

def is_valid_grade(grade_str: str) -> bool:
    try:
        g = int(grade_str)
        return 1 <= g <= 5
    except ValueError:
        return False

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(10)

print(f"Journal HTTP server started on http://{HOST}:{PORT}/")

while True:
    conn, addr = server_socket.accept()
    try:
        method, path, headers, body = parse_http_request(conn)
        journal = load_journal()

        if method == "GET":
            page = render_page(journal)
            conn.sendall(http_response(page))

        elif method == "POST":
            form = urllib.parse.parse_qs(body.decode("utf-8", errors="ignore"))

            subject = (form.get("subject", [""])[0]).strip()
            grade = (form.get("grade", [""])[0]).strip()

            if not subject or not grade or not is_valid_grade(grade):
                page = "<h1>400 Bad Request</h1><p>Нужно передать subject и grade (оценка 1..5).</p>"
                conn.sendall(http_response(page, status="400 Bad Request"))
            else:
                journal.setdefault(subject, [])
                journal[subject].append(int(grade))
                save_journal(journal)

                page = render_page(journal)
                conn.sendall(http_response(page))

        else:
            conn.sendall(http_response("<h1>405 Method Not Allowed</h1>", status="405 Method Not Allowed"))

    except Exception as e:
        conn.sendall(http_response(f"<h1>500</h1><pre>{e}</pre>", status="500 Internal Server Error"))
    finally:
        conn.close()