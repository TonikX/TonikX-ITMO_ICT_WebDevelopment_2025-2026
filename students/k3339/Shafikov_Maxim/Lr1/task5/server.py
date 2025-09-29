import socket
import urllib.parse
from collections import defaultdict
from students.k3339.Shafikov_Maxim.Lr1.config import host, port


grades = defaultdict(list)


def render_html():
    rows = ""
    if grades:
        for subj, marks in grades.items():
            avg = sum(marks) / len(marks)
            marks_str = ", ".join(str(m) for m in marks)
            rows += f"<tr><td>{subj}</td><td>{marks_str}</td><td>{avg:.2f}</td></tr>\n"
    else:
        rows = '<tr><td colspan="3">Пока нет оценок</td></tr>'

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>Оценки по дисциплинам</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 40px; }}
    table {{ border-collapse: collapse; width: 500px; margin-bottom: 20px; }}
    th, td {{ border: 1px solid #333; padding: 8px; text-align: center; }}
    th {{ background: #eee; }}
    form {{ display: flex; flex-direction: column; width: 400px; gap: 10px; }}
    label {{ display: flex; justify-content: space-between; }}
    input[type=text], input[type=number] {{ flex: 1; margin-left: 10px; }}
    input[type=submit] {{ padding: 8px; font-size: 16px; }}
  </style>
</head>
<body>
  <h1>Оценки по дисциплинам</h1>
  <table>
    <tr><th>Дисциплина</th><th>Оценки</th><th>Средняя</th></tr>
    {rows}
  </table>
  <form method="POST">
    <label>Дисциплина: <input type="text" name="subject" required></label>
    <label>Оценка (1-5): <input type="number" name="grade" min="1" max="5" required></label>
    <input type="submit" value="Добавить">
  </form>
</body>
</html>"""


def handle_request(request: str):
    lines = request.split("\r\n")
    if not lines:
        return "HTTP/1.1 400 Bad Request\r\n\r\n"

    first_line = lines[0]
    method, *_ = first_line.split()

    if method == "POST":
        body = request.split("\r\n\r\n", 1)[-1]
        data = urllib.parse.parse_qs(body)
        subject = data.get("subject", [""])[0].strip()
        grade_str = data.get("grade", [""])[0].strip()

        if subject and grade_str.isdigit():
            grade = int(grade_str)
            if 1 <= grade <= 5:
                grades[subject].append(grade)

    body = render_html()
    headers = [
        "HTTP/1.1 200 OK",
        "Content-Type: text/html; charset=utf-8",
        f"Content-Length: {len(body.encode("utf-8"))}",
        "Connection: close",
        "",
        ""
    ]
    return "\r\n".join(headers) + body


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
        tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_socket.bind((host, port))
        tcp_socket.listen(5)
        print(f"Сервер слушает на http://{host}:{port}")

        while True:
            conn, addr = tcp_socket.accept()
            print(f"[+] Подключение от {addr[0]}:{addr[1]}")
            with conn:
                request = conn.recv(4096).decode("utf-8", errors="ignore")
                if not request:
                    continue
                response = handle_request(request)
                conn.sendall(response.encode("utf-8"))


if __name__ == "__main__":
    main()
