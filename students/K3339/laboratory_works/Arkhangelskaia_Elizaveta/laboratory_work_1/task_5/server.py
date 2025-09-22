import socket
from urllib.parse import parse_qs

HOST = '127.0.0.1'
PORT = 8080

grades = dict()


def generate_html():
    html = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
    <meta charset="UTF-8">
    <title>Оценки по дисциплинам</title>
    <style>
        body {
            text-align: center;
            font-family: Arial, sans-serif;
            padding: 20px;
        }
        h1, h3{
            color: #d6336c;
        }
        form {
            display: inline-block;
            text-align: left;
            margin-top: 20px;
            padding: 20px 25px;
            background: #ffffff;
            border-radius: 12px;
            border: 1px solid #f5c2c7;
        }
        label {
            display: block;
            margin-bottom: 15px;
            font-weight: bold;
            color: #333;
        }
        input[type="text"] {
            width: 92%;
            padding: 8px 10px;
            margin-top: 5px;
            border: 1px solid #ced4da;
            border-radius: 6px;
        }
        input[type="submit"] {
            display: block;
            width: 100%;
            padding: 10px;
            background: #d6336c;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
        }
        input[type="submit"]:hover {
            background: #b02a50;
        }
        .grades {
            display: inline-block;
        }
        .grades li {
            padding: 5px 5px;
        }
        </style>
        </head>
    <body>
    <h1>Оценки по дисциплинам</h1>
    <form method="POST">
        <label> Дисциплина: <input type="text" name="subject" required></label>
        <label> Оценка: <input type="text" name="grade" required></label>
        <input type="submit" value="Добавить">
    </form>
    <h3>Все оценки:</h3>
    <ul class="grades">
    """
    for item in sorted(grades):
        html += f"<li>{item}: " + ", ".join(grades[item])+ "</li>"
    html += """
        </ul>
    </body>
    </html>
    """
    return html


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"Сервер запущен на http://{HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            with conn:
                request = conn.recv(1024).decode('utf-8')
                if not request:
                    continue
                try:
                    headers = request.split('\r\n')
                    method, path, _ = headers[0].split()
                except ValueError:
                    continue

                if method == "POST":
                    body = request.split('\r\n\r\n')[1]
                    data = parse_qs(body)
                    subject = data.get('subject', [''])[0]
                    grade = data.get('grade', [''])[0]
                    if subject not in grades:
                        grades[subject] = [grade]
                    else:
                        grades[subject].append(grade)

                response_body = generate_html()
                response = (
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: text/html; charset=utf-8\r\n"
                        f"Content-Length: {len(response_body.encode('utf-8'))}\r\n"
                        "Connection: close\r\n"
                        "\r\n" +
                        response_body
                )

                conn.sendall(response.encode('utf-8'))

if __name__ == '__main__':
    main()