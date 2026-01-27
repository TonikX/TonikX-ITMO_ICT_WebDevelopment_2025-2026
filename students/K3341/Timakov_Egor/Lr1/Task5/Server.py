import socket
import threading
from urllib.parse import parse_qs


HOST = '127.0.0.1'
PORT = 8080
# Словарь для хранения данных: {'Дисциплина': 'Оценка'}
grades_data = {}

# Блокировка для безопасной работы с общими данными (grades_data) в многопоточной среде
data_lock = threading.Lock()



def build_response(status_code, content_type, body):
    """Формирует полный HTTP-ответ."""
    if status_code == 200:
        status_line = "HTTP/1.1 200 OK\r\n"
    elif status_code == 303:
        # 303 See Other для перенаправления после успешного POST
        status_line = "HTTP/1.1 303 See Other\r\n"
    else:
        status_line = "HTTP/1.1 404 Not Found\r\n"

    headers = (
            status_line +
            f"Content-Type: {content_type}; charset=utf-8\r\n"
            f"Content-Length: {len(body.encode('utf-8'))}\r\n"
            "Connection: close\r\n"
    )

    # Добавляем заголовок для перенаправления после POST
    if status_code == 303:
        headers += "Location: /\r\n"

    return (headers + "\r\n" + body).encode('utf-8')


def get_html_page():
    """Генерирует HTML-страницу для GET-запроса, включая форму и таблицу оценок."""

    # Генерация таблицы с оценками
    table_rows = ""
    with data_lock:
        if grades_data:
            for discipline, grade in grades_data.items():
                table_rows += f"<tr><td>{discipline}</td><td>{grade}</td></tr>"
        else:
            table_rows = '<tr><td colspan="2">Оценок пока нет.</td></tr>'

    html = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Система Учета Оценок (Socket)</title>
    <style>
        body {{ font-family: sans-serif; margin: 40px; }}
        table {{ border-collapse: collapse; width: 50%; margin-top: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        form {{ margin-bottom: 30px; padding: 20px; border: 1px solid #ccc; }}
        input[type="text"] {{ padding: 8px; margin-right: 10px; }}
        input[type="submit"] {{ padding: 8px 15px; cursor: pointer; }}
    </style>
</head>
<body>
    <h1>Учет Оценок</h1>

    <h2>Добавить новую оценку</h2>
    <form method="POST" action="/">
        <label for="discipline">Дисциплина:</label>
        <input type="text" id="discipline" name="discipline" required>

        <label for="grade">Оценка:</label>
        <input type="text" id="grade" name="grade" required>

        <input type="submit" value="Сохранить">
    </form>

    <h2>Текущие оценки</h2>
    <table>
        <thead>
            <tr>
                <th>Дисциплина</th>
                <th>Оценка</th>
            </tr>
        </thead>
        <tbody>
            {table_rows}
        </tbody>
    </table>
</body>
</html>
"""
    return html


def handle_request(conn, addr):
    """Обрабатывает входящий запрос от клиента."""
    try:
        # Принимаем данные
        request_data = conn.recv(4096).decode('utf-8')
        if not request_data:
            return

        # Парсим первую строку запроса для определения метода и пути
        first_line = request_data.split('\n')[0].strip()
        method, path, _ = first_line.split()

        print(f"[{addr[0]}:{addr[1]}] {method} {path}")

        if method == 'GET':
            # 1. Обработка GET запроса
            if path == '/':
                html_body = get_html_page()
                response = build_response(200, "text/html", html_body)
            else:
                response = build_response(404, "text/html", "<h1>404 Not Found</h1>")

            conn.sendall(response)

        elif method == 'POST':
            # 2. Обработка POST запроса
            if path == '/':
                # Находим тело POST-запроса (после пустой строки)
                body_start = request_data.find('\r\n\r\n') + 4
                post_body = request_data[body_start:].strip()

                # Парсим данные из тела запроса
                params = parse_qs(post_body)

                discipline = params.get('discipline', [''])[0].strip()
                grade = params.get('grade', [''])[0].strip()

                if discipline and grade:
                    with data_lock:
                        grades_data[discipline] = grade
                    print(f"Сохранена новая оценка: {discipline} -> {grade}")

                    # Отправляем 303 Redirect, чтобы избежать повторной отправки формы
                    response = build_response(303, "text/html", "")
                else:
                    response = build_response(200, "text/html", "<h1>Ошибка: Неполные данные</h1>")

                conn.sendall(response)

            else:
                response = build_response(404, "text/html", "<h1>404 Not Found</h1>")
                conn.sendall(response)

        else:
            # Обработка неподдерживаемых методов
            conn.sendall(build_response(405, "text/html", "<h1>405 Method Not Allowed</h1>"))

    except Exception as e:
        print(f"Ошибка при обработке запроса: {e}")
    finally:
        conn.close()




def start_server():
    """Запуск многопоточного TCP-сервера."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
    except Exception as e:
        print(f"Не удалось запустить сервер: {e}")
        return

    print(f"Сервер запущен. Откройте в браузере: http://{HOST}:{PORT}/")
    print("Ожидание подключений...")

    try:
        while True:
            # Принимаем соединение
            conn, addr = server_socket.accept()

            # Запускаем обработку запроса в отдельном потоке
            thread = threading.Thread(target=handle_request, args=(conn, addr))
            thread.start()

    except KeyboardInterrupt:
        print("\nСервер остановлен пользователем.")
    except Exception as e:
        print(f"Общая ошибка сервера: {e}")
    finally:
        server_socket.close()
        print("Серверный сокет закрыт.")


if __name__ == "__main__":
    start_server()