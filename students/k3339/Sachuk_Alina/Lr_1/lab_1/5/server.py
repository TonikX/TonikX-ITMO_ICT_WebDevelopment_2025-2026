import socket
from urllib.parse import unquote_plus

grades = {}


def generate_html():
    html = """
    <html>
        <head>
            <meta charset='UTF-8'>
            <title>Журнал</title>
        </head>
        <body>
            <h1>Журнал оценок</h1>
            <form method="POST">
                <label for="subject">Предмет:</label>
                <input type="text" id="subject" name="subject" required>
                <label for="grade">Оценка:</label>
                <input type="text" id="grade" name="grade" required>
                <button type="submit">Добавить оценку</button>
            </form>
            <h2>Журнал</h2>
            <table border="1">
                <tr>
                    <th>Предмет</th>
                    <th>Оценки</th>
                </tr>
    """
    for subject, grade_list in grades.items():
        grades_str = ", ".join(grade_list)
        html += f"<tr><td>{subject}</td><td>{grades_str}</td></tr>"

    html += """
            </table>
        </body>
    </html>
    """
    return html


def parse_post_data(body):
    post_data = {}
    if not body:
        return post_data
    params = body.split('&')
    for param in params:
        if '=' in param:
            key, value = param.split('=', 1)
            post_data[key] = unquote_plus(value)
    return post_data


def handle_request(method, headers, body):
    if method == 'POST':
        post_data = parse_post_data(body)
        subject = post_data.get('subject', '').strip()
        grade = post_data.get('grade', '').strip()

        if subject and grade:
            if subject in grades:
                grades[subject].append(grade)
            else:
                grades[subject] = [grade]

        return "HTTP/1.1 303 See Other\r\nLocation: /\r\n\r\n"

    response_body = generate_html()
    response = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n' + response_body
    return response


def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(5)
    print("Сервер запущен на порту 8080...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Получен запрос от {addr}")

        request_data = client_socket.recv(1024).decode('utf-8')

        if request_data:
            headers, _, body = request_data.partition('\r\n\r\n')
            header_lines = headers.splitlines()
            request_line = header_lines[0]
            method, path, _ = request_line.split()

            content_length = 0
            for line in header_lines:
                if line.lower().startswith("content-length:"):
                    content_length = int(line.split(":")[1].strip())
                    break

            if content_length > 0 and len(body) < content_length:
                body += client_socket.recv(content_length - len(body)).decode("utf-8")

            response = handle_request(method, headers, body)
            client_socket.sendall(response.encode('utf-8'))

        client_socket.close()


if __name__ == "__main__":
    run_server()
