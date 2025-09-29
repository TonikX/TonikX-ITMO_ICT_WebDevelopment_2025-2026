import socket
import urllib.parse
import threading

# Хранилище: дисциплина -> список оценок
grades = {}

HOST = "127.0.0.1"
PORT = 8080

def build_html():
    # Формирует HTML-страницу с таблицей и формой
    rows = ""
    if grades:
        for discipline, marks in grades.items():
            rows += f"<tr><td>{discipline}</td><td>{', '.join(marks)}</td></tr>"
    else:
        rows = "<tr><td colspan='2'>Пока нет оценок</td></tr>"

    return f"""
    <html>
        <head>
            <meta charset="utf-8">
            <title>Оценки</title>
        </head>
        <body>
            <h1>Список оценок</h1>
            <table border="1" cellpadding="5">
                <tr><th>Дисциплина</th><th>Оценки</th></tr>
                {rows}
            </table>
            <h2>Добавить оценку</h2>
            <form method="POST">
                Дисциплина: <input type="text" name="discipline"><br>
                Оценка: <input type="text" name="grade"><br>
                <input type="submit" value="Добавить">
            </form>
        </body>
    </html>
    """

def handle_request(request: str, post_request_is_active: bool):
    # Обработка HTTP-запроса
    lines = request.split("\r\n")
    if not lines:
        return "HTTP/1.1 400 Bad Request\r\n\r\n", post_request_is_active

    method = lines[0].split(" ")[0]

    print("method =", method, post_request_is_active)

    if method == "GET":
        # возвращаем страницу
        body = build_html()
        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type: text/html; charset=utf-8\r\n"
        response += f"Content-Length: {len(body.encode('utf-8'))}\r\n"
        response += "\r\n"
        response += body
        post_request_is_active = False
        return response, post_request_is_active
    
    if method == "POST":
        post_request_is_active = True

    if post_request_is_active:
        header_and_body = request.split("\r\n\r\n")
        
        body = header_and_body[len(header_and_body) - 1]
        
        data = urllib.parse.parse_qs(body)
        discipline = data.get("discipline", [""])[0].strip()
        grade = data.get("grade", [""])[0].strip()
        if discipline and grade:
            grades.setdefault(discipline, []).append(grade)
            post_request_is_active = False
            response = "HTTP/1.1 302 Found\r\nLocation: /\r\n\r\n"
            return response, post_request_is_active
    
    return "", post_request_is_active

def single_client_processing(conn, addr):
    print("Connected by", addr)
    with conn:
        post_request_is_active = False
        while True:
            request = conn.recv(1024).decode("utf-8", errors="ignore")
            if not request:
                continue
            
            print()
            print("========================", "Request from", addr, "========================")
            print(request)
            print("================================================")
            response, post_request_is_active = handle_request(request, post_request_is_active)
            if response != "":
                conn.sendall(response.encode("utf-8"))
            print()

    print("Connection closed", addr)

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Сервер запущен: http://{HOST}:{PORT}")

        while True:
            client_socket, addr = server_socket.accept()
            client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            thread = threading.Thread(target=single_client_processing,  args=[client_socket, addr])
            thread.start()

if __name__ == "__main__":
    run_server()
