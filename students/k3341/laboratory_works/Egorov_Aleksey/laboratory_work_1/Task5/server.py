import socket
from urllib.parse import parse_qs

HOST = '127.0.0.1'
PORT = 9090

grades = []


def handle_request(request):
    lines = request.split('\r\n')
    if len(lines) < 1:
        return "HTTP/1.1 400 Bad Request\r\n\r\n"

    request_line = lines[0]
    try:
        method, path, _ = request_line.split()
    except ValueError:
        return "HTTP/1.1 400 Bad Request\r\n\r\n"

    if method == "GET":
        response_body = "<html><body><h2>Список оценок</h2><ul>"
        for grade in grades:
            response_body += f"<li>{grade['subject']}: {grade['mark']}</li>"
        response_body += "</ul>"
        response_body += '''
            <h3>Добавить новую оценку</h3>
            <form method="POST">
                Предмет: <input name="subject"><br>
                Оценка: <input name="mark"><br>
                <input type="submit" value="Добавить">
            </form>
        '''
        response_body += "</body></html>"

        response = (
            "HTTP/1.1 200 OK\r\n"
            f"Content-Length: {len(response_body.encode())}\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            "\r\n"
            + response_body
        )
        return response

    elif method == "POST":
        try:
            empty_line_index = lines.index('')
            body = '\r\n'.join(lines[empty_line_index + 1:])
        except ValueError:
            body = lines[-1]

        data = parse_qs(body)
        subject = data.get("subject", [""])[0]
        mark = data.get("mark", [""])[0]

        if subject and mark:
            grades.append({"subject": subject, "mark": mark})

        response = (
            "HTTP/1.1 303 See Other\r\n"
            "Location: /\r\n"
            "Content-Length: 0\r\n"
            "\r\n"
        )
        return response

    else:
        return "HTTP/1.1 405 Method Not Allowed\r\n\r\n"


def main():
    sock = socket.socket()
    sock.bind((HOST, PORT))
    sock.listen(1)

    print(f"Сервер запущен {HOST}:{PORT}")

    while True:
        conn, addr = sock.accept()
        print('Подключение:', addr)

        request = b""
        while True:
            part = conn.recv(1024)
            if not part:
                break
            request += part
            if len(part) < 1024:
                break
        request = request.decode()
        print("Полученный запрос:\n", request)

        response = handle_request(request)
        conn.sendall(response.encode())
        conn.close()

if __name__ == "__main__":
    main()

# http://localhost:9090/