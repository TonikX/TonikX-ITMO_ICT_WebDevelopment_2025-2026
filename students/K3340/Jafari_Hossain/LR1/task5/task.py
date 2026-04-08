import socket
import threading
import urllib.parse  # Для разбора данных формы POST

# Словарь для хранения предметов и списка оценок
grades = {}  # key = предмет, value = список оценок

# Функция для генерации HTML страницы с таблицей оценок и формой добавления
def generate_html():
    html = """
    <html>
    <head><title>Grades</title></head>
    <body>
        <h1>Grades List</h1>
        <table border="1" cellpadding="5" cellspacing="0">
            <tr><th>Subject</th><th>Grades</th></tr>
    """
    # Добавляем строки таблицы для каждого предмета
    for subject, grade_list in grades.items():
        grades_str = ", ".join(grade_list)  # Все оценки через запятую
        html += f"<tr><td>{subject}</td><td>{grades_str}</td></tr>"

    # Добавляем HTML-форму для добавления новой оценки
    html += """
        </table>
        <br>
        <form method="POST" action="/">
            <input type="text" name="subject" placeholder="Subject" required><br>
            <input type="text" name="grade" placeholder="Grade" required><br>
            <input type="submit" value="Add Grade">
        </form>
    </body>
    </html>
    """
    return html  # Возвращаем сформированный HTML

# Функция обработки HTTP-запроса от клиента
def handle_request(client_socket):
    request = client_socket.recv(1024).decode('utf-8')  # Получаем запрос клиента
    print(f"Received request:\n{request}")

    if not request:  # Если пустой запрос, закрываем соединение
        client_socket.close()
        return

    # Получаем метод запроса (GET или POST)
    lines = request.split("\r\n")
    method, path, _ = lines[0].split()

    if method == "POST":
        # Ищем длину тела запроса (Content-Length)
        content_length = 0
        for line in lines:
            if line.startswith("Content-Length:"):
                content_length = int(line.split(": ")[1])
                break

        # Получаем тело POST-запроса
        body = request.split("\r\n\r\n", 1)[1]
        if len(body) < content_length:
            body += client_socket.recv(content_length - len(body)).decode("utf-8")

        # Разбираем данные формы
        params = urllib.parse.parse_qs(body)
        subject = params.get("subject", [""])[0].strip()
        grade = params.get("grade", [""])[0].strip()

        if subject and grade:
            # Если предмет уже есть — добавляем оценку в список, иначе создаем новый список
            if subject not in grades:
                grades[subject] = []
            grades[subject].append(grade)

    # Формируем HTML для ответа
    html_content = generate_html()
    response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + html_content
    client_socket.sendall(response.encode("utf-8"))  # Отправляем ответ клиенту
    client_socket.close()  # Закрываем соединение

# Функция запуска сервера
def start_server(host="localhost", port=8080):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Создаем TCP сокет
    server_socket.bind((host, port))  # Привязываем сокет к хосту и порту
    server_socket.listen(5)  # Начинаем прослушивание до 5 соединений
    print(f"Server started at http://{host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()  # Принимаем новое соединение
        print(f"Connection from {client_address}")
        # Запускаем обработку запроса в отдельном потоке
        threading.Thread(target=handle_request, args=(client_socket,)).start()


if __name__ == "__main__":
    start_server()  # Запуск сервера
