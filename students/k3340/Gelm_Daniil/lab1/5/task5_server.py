import socket
import urllib.parse

grades = {}

def generate_html():
    html = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Журнал оценок</title>
    <style>
        body { font-family: Arial; margin: 20px; }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        form { margin-bottom: 20px; }
        input, button { padding: 5px; margin: 5px; }
    </style>
</head>
<body>
    <h1>Журнал оценок</h1>
    <form method="POST" action="/">
        <input type="text" name="discipline" placeholder="Дисциплина" required>
        <input type="number" name="grade" placeholder="Оценка" min="1" max="5" required>
        <button type="submit">Добавить оценку</button>
    </form>
    <table>
        <tr>
            <th>Дисциплина</th>
            <th>Оценки</th>
        </tr>"""
    
    for discipline, grade_list in grades.items():
        grades_str = ', '.join(map(str, grade_list))
        html += f"<tr><td>{discipline}</td><td>{grades_str}</td></tr>"
    
    html += """</table>
</body>
</html>"""
    return html

def parse_post(data):
    params = {}
    if '\r\n\r\n' in data:
        parts = data.split('\r\n\r\n', 1)
        if len(parts) > 1:
            body = parts[1]
            for pair in body.split('&'):
                if '=' in pair:
                    key, value = pair.split('=', 1)
                    params[urllib.parse.unquote(key)] = urllib.parse.unquote(value)
    return params

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8892))
server_socket.listen(5)

print("Веб-сервер запущен на порту 8892")

while True:
    client_socket, addr = server_socket.accept()
    request = client_socket.recv(4096).decode('utf-8')
    
    if request.startswith('POST'):
        params = parse_post(request)
        discipline = params.get('discipline', '')
        grade = params.get('grade', '')
        
        if discipline and grade:
            if discipline not in grades:
                grades[discipline] = []
            grades[discipline].append(int(grade))
    
    html_content = generate_html()
    
    response = "HTTP/1.1 200 OK\r\n"
    response += "Content-Type: text/html; charset=utf-8\r\n"
    response += f"Content-Length: {len(html_content.encode('utf-8'))}\r\n"
    response += "\r\n"
    response += html_content
    
    client_socket.send(response.encode('utf-8'))
    client_socket.close()

