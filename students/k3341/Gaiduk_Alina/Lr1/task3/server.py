import socket

def load_html(filename: str) -> tuple[str, int]:
    try:
        with open(filename, "r", encoding="UTF-8") as file:
            return file.read(), 200
    except FileNotFoundError:
        return "<h1>404 Not Found</h1><p>Файл index.html не найден.</p>", 404

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Разрешаем повторно использовать порт (при перезапуске сервера)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('127.0.0.1', 11111))
        server_socket.listen()
        print("Сервер запущен по адресу: http://127.0.0.1:11111")

        while True:
            # Ждем подключения
            client_socket, client_address = server_socket.accept()
            with client_socket:
                # Получаем от клиента HTTP-запрос
                request = client_socket.recv(1024).decode("UTF-8")
                request_line = request.split("\r\n", 1)[0]
                method = request_line.split(" ")[0] if request_line else ""

                if method != "GET":
                    html_content = "<h1>405 Method Not Allowed</h1>"
                    status_line = "HTTP/1.1 405 Method Not Allowed"
                else:
                    html_content, status_code = load_html("index.html")
                    if status_code == 200:
                        status_line = "HTTP/1.1 200 OK"
                    else:
                        status_line = "HTTP/1.1 404 Not Found"

                # Формируем HTTP-ответ с заголовками и HTML-контентом
                response = (
                    f"{status_line}\r\n" # статусная строка
                    "Content-Type: text/html; charset=UTF-8\r\n" # как интерпретировать данные
                    f"Content-Length: {len(html_content.encode('UTF-8'))}\r\n" # длина содержимого в байтах
                    "Connection: close\r\n" # после ответа сервер закрывает соединение
                    "\r\n" # строка, разделяющая заголовки и тело ответа
                    f"{html_content}" # тело ответа
                )
                # Отправляем HTTP-ответ клиенту
                client_socket.sendall(response.encode("UTF-8"))

if __name__ == "__main__":
    run_server()

