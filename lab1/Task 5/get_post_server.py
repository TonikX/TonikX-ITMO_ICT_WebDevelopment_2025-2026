import socket
from urllib.parse import unquote_plus  # Для декодирования данных формы из URL-кодировки

HOST = "localhost"
PORT = 8080

grades = {}  # Словарь для хранения оценок по дисциплинам

def build_html():
    """Создает HTML-страницу с формой и таблицей оценок"""
    # Генерируем строки таблицы с текущими оценками
    rows = "".join(f"<tr><td>{subject}</td><td>{grade}</td></tr>" for subject, grade in grades.items())
    html = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Оценки по дисциплинам</title>
    </head>
    <body>
        <h1>Добавить оценку</h1>
        <form method="POST" action="/">
            Дисциплина: <input type="text" name="subject" required>
            Оценка: <input type="text" name="grade" required>
            <input type="submit" value="Добавить">
        </form>
        <h2>Все оценки</h2>
        <table border="1">
            <tr><th>Дисциплина</th><th>Оценка</th></tr>
            {rows}
        </table>
    </body>
    </html>
    """
    return html

def parse_post_data(body):
    data = {}
    for pair in body.split("&"):  # Каждая пара key=value
        if "=" in pair:
            key, value = pair.split("=", 1)
            data[key] = unquote_plus(value)  # Декодируем URL-кодировку
    return data

def handle_client(conn):
    try:
        request = conn.recv(4096).decode("utf-8")  # Получаем HTTP-запрос
        if not request:
            return
        headers, _, body = request.partition("\r\n\r\n")  # Разделяем заголовки и тело
        first_line = headers.splitlines()[0]  # Берем первую строку запроса
        method, path, _ = first_line.split()

        if method == "POST":
            post_data = parse_post_data(body)  # Разбираем данные формы
            subject = post_data.get("subject", "").strip()
            grade = post_data.get("grade", "").strip()
            if subject and grade:
                grades[subject] = grade  # Сохраняем оценку

        # Формируем HTML-ответ
        html_content = build_html()
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(html_content.encode('utf-8'))}\r\n"
            "\r\n"
            f"{html_content}"
        )
        conn.sendall(response.encode("utf-8"))  # Отправляем клиенту
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        conn.close()  # Закрываем соединение

# Настройка TCP-сокета сервера
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((HOST, PORT))
server_sock.listen(5)  # Максимум 5 ожидающих подключений
print(f"Сервер оценок запущен на http://{HOST}:{PORT}")

try:
    while True:
        conn, addr = server_sock.accept()  # Ожидаем подключение клиента
        handle_client(conn)  # Обрабатываем запрос
except KeyboardInterrupt:
    print("\nСервер завершён")
finally:
    server_sock.close()
