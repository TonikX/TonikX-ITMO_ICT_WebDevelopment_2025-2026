import socket

marks = {}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8082))
server.listen()
print('Сервер журнала оценок запущен… http://localhost:8082' )

while True:
    client, addr = server.accept()
    request = client.recv(1024).decode()

    if "GET" in request:
        body = """
        <html>
        <head><title>Журнал оценок</title></head>
        <body>
        <h2>Добавь оценку через POST (curl/Postman)!</h2>
        <h3>Текущий журнал:</h3>
        <ul>
        """
        for subj, grades in marks.items():
            body += f"<li>{subj}: {', '.join(grades)}</li>"
        body += "</ul></body></html>"
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n" + body
    elif "POST" in request:

        if '\r\n\r\n' in request:
            post_data = request.split('\r\n\r\n', 1)[1]
            parts = post_data.split('&')
            subj, grade = "", ""
            for part in parts:
                if "subj=" in part:
                    subj = part.split('=')[1]
                if "grade=" in part:
                    grade = part.split('=')[1]
            if subj and grade:
                marks.setdefault(subj, []).append(grade)
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\nОценка добавлена!"
    else:
        response = "HTTP/1.1 400 Bad Request\r\nContent-Type: text/plain\r\n\r\nОшибка запроса!"
    client.send(response.encode())
    client.close()
