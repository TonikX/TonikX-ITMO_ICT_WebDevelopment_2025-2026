import socket

journal = {}


def generate_html():
    global journal
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Data page</title>
</head>
<body>
    <h1>Task 5</h1>
    <h3>made by Alexey Bazhenov</h3>
    <br>
    <hr>
    <h2>Marks for disciplines:</h2>'''

    if journal:
        for discipline, mark_list in journal.items():
            marks_str = " ".join(str(mark) for mark in mark_list)
            html_content += f'<p>{discipline}: {marks_str}</p><hr>'
    else:
        html_content += '<p>No marks</p><hr>'

    html_content += '</body></html>'
    return html_content


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('localhost', 8080))

server_socket.listen(5)
print("Сервер запущен на порту 8080...")

while True:
    client_connection, client_address = server_socket.accept()
    print(f'Запрос от {client_address}')

    request = client_connection.recv(1024)
    data = request.decode('utf-8')

    if request.startswith('GET'.encode()):
        html_content = generate_html()
        response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=utf-8\r\n"
                f"Content-Length: {len(html_content)}\r\n"
                "\r\n" + html_content
        )
        client_connection.sendall(response.encode('utf-8'))

    elif request.startswith('POST'.encode()):
        lines = request.decode().split('\r\n')
        post_data = ""
        for i, line in enumerate(lines):
            if line == '' and i + 1 < len(lines):
                post_data = lines[i + 1]
                break
        if 'discipline=' in post_data and 'mark=' in post_data:
            params = post_data.split('&')
            discipline = None
            mark = None
            for param in params:
                if param.startswith('discipline='):
                    discipline = param[11:]
                elif param.startswith('mark='):
                    mark = param[5:]
            print(discipline, mark)
            if discipline not in journal.keys():
                journal[discipline] = []
            journal[discipline].append(mark)

        else:
            response = "HTTP/1.1 400 Bad Request\r\n\r\nОтсутствуют параметры discipline или mark"
            client_connection.sendall(response.encode('utf-8'))
            client_connection.close()
            continue

        html = open("success.html", 'r').read()
        response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=utf-8\r\n"
                f"Content-Length: {len(html)}\r\n"
                "\r\n" + html
        )
        client_connection.sendall(response.encode('utf-8'))

    else:
        response = "HTTP/1.1 405 Method Not Allowed\r\n\r\nMethod not supported"

    client_connection.close()
    print("запрос успешно обработан")