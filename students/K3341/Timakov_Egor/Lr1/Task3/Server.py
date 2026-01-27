import socket

# Конфигурация сервера
HOST = '127.0.0.1'
PORT = 8090
HTML_FILE = 'index.html'


def start_server():
    """Запускает простой HTTP-сервер на сокетах."""

    # 1. Загрузка содержимого HTML-файла
    try:
        with open(HTML_FILE, 'r', encoding='utf-8') as f:
            html_content = f.read()

    except FileNotFoundError:
        print(f"Ошибка: Файл '{HTML_FILE}' не найден. Убедитесь, что он находится в той же директории.")
        return

    # Формирование полного HTTP-ответа
    # Строка статуса: HTTP/1.1 200 OK
    # Заголовки: Content-Type и Content-Length
    http_response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(html_content.encode('utf-8'))}\r\n"
        "Connection: close\r\n"  # Закрываем соединение после ответа
        "\r\n" 
        f"{html_content}"
    )

    # 2. Создание и настройка сокета
    print(f"Сервер запускается на {HOST}:{PORT}...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Позволяет повторно использовать адрес сразу после закрытия
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Привязка сокета к адресу и порту
        server_socket.bind((HOST, PORT))

        # Прослушивание входящих соединений
        server_socket.listen(1)
        print("Сервер запущен. Ожидание соединения...")

        try:
            while True:
                # 3. Принятие соединения
                conn, addr = server_socket.accept()
                with conn:
                    print(f"\nПолучено соединение от {addr}")

                    # 4. Получение HTTP-запроса от клиента (браузера)
                    request = conn.recv(1024).decode('utf-8')
                    if not request:
                        continue

                    # 5. Отправка HTTP-ответа
                    conn.sendall(http_response.encode('utf-8'))
                    print(f"Ответ (файл {HTML_FILE}) отправлен.")

        except KeyboardInterrupt:
            print("\nСервер остановлен пользователем.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")
        finally:
            server_socket.close()
            print("Сокет закрыт.")


if __name__ == '__main__':
    start_server()
