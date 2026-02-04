import socket

# Параметры сервера
HOST = 'localhost'
PORT = 8080

# Создаем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"HTTP сервер запущен на {HOST}:{PORT}...")

# Функция для чтения HTML-файла
def load_html_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        # Если файл не найден, возвращаем простую ошибку 404
        return "<h1>404 Not Found</h1><p>Файл index.html не найден.</p>"

while True:
    client_connection, client_address = server_socket.accept()
    print(f'Подключение от {client_address}')

    request = client_connection.recv(1024).decode()
    print(f'Запрос клиента:\n{request}')

    # Загружаем содержимое index.html
    html_content = load_html_file('index.html')

    # Формируем HTTP-ответ
    http_response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=UTF-8\r\n"
        f"Content-Length: {len(html_content)}\r\n"
        "Connection: close\r\n"
        "\r\n"
        + html_content
    )

    client_connection.sendall(http_response.encode())
    client_connection.close()