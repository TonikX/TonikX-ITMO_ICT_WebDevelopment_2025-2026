import socket
from datetime import datetime

def load_html_file(file_name):
    """Читает содержимое HTML-файла и возвращает (текст, найден_ли_файл: bool)."""
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            return file.read(), True
    except FileNotFoundError:
        not_found_html = "<!doctype html><meta charset='utf-8'><h1>404 - File Not Found</h1>"
        return not_found_html, False

def build_http_response(status_code, body_text):
    """Формирует корректное HTTP-сообщение (заголовки + тело)."""
    if status_code == 200:
        status_line = "HTTP/1.1 200 OK"
    elif status_code == 404:
        status_line = "HTTP/1.1 404 Not Found"
    else:
        status_line = f"HTTP/1.1 {status_code}"

    body_bytes = body_text.encode("utf-8")
    headers = [
        status_line,
        "Content-Type: text/html; charset=utf-8",
        f"Content-Length: {len(body_bytes)}",     # длина в байтах!
        "Connection: close",
        f"Date: {datetime.utcnow():%a, %d %b %Y %H:%M:%S} GMT",
    ]
    # Между заголовками и телом обязательно должна быть пустая строка (\r\n\r\n)
    response_text = "\r\n".join(headers) + "\r\n\r\n"
    return response_text.encode("utf-8") + body_bytes

def main():
    server_host = "127.0.0.1"
    server_port = 8081
    html_file_name = "index.html"

    # Создаем TCP-сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Чтобы можно было быстро перезапускать сервер на том же порту
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((server_host, server_port))

    # Начинаем прослушивание входящих подключений
    server_socket.listen(5)
    print(f"HTTP-сервер запущен на http://{server_host}:{server_port}")

    try:
        while True:
            try:
                # Принимаем подключение
                client_socket, client_address = server_socket.accept()
                print(f"Подключился клиент: {client_address}")

                # Получаем HTTP-запрос
                raw_request = client_socket.recv(2048).decode("utf-8", errors="ignore")
                print(f"Получен запрос:\n{raw_request}")

                # Загружаем HTML-страницу из файла
                html_content, file_found = load_html_file(html_file_name)

                # Готовим ответ с корректным статусом
                status_code = 200 if file_found else 404
                http_response = build_http_response(status_code, html_content)

                # Отправляем ответ клиенту
                client_socket.sendall(http_response)
                print(f"Отправлен HTTP-ответ со статусом {status_code}\n")

            except KeyboardInterrupt:
                print("\nСервер остановлен")
                break
            except Exception as error:
                print(f"Произошла ошибка при обработке клиента: {error}")
            finally:
                try:
                    client_socket.close()
                except Exception:
                    pass
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
