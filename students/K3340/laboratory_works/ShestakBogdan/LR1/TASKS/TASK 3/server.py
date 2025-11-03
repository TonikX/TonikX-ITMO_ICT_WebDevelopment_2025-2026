import socket  # Импортируем модуль для работы с сетевыми сокетами
import os      # Импортируем модуль для работы с файловой системой

# Создаем TCP-сокет (SOCK_STREAM) и привязываем его к адресу, чтобы слушать подключения
sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_server.bind(('localhost', 8080))  # Привязываем сокет к localhost:8080
sock_server.listen(1)  # Переводим сокет в режим прослушивания, с очередью 1 подключение
print("Server on...")  # Выводим сообщение, что сервер запущен

# Определяем путь к файлу index.html, который будем отдавать клиенту
base_dir = os.path.dirname(os.path.abspath(__file__))  # Директория текущего скрипта
file_path = os.path.join(base_dir, "index.html")       # Полный путь к index.html

while True:  # Бесконечный цикл для обработки подключений
    # Принимаем подключение от клиента
    client_connection, client_address = sock_server.accept()
    print(f"Client {client_address}")  # Выводим адрес подключившегося клиента

    # Открываем HTML-файл и читаем его содержимое
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()  # Читаем весь файл в строку

    # Формируем HTTP-ответ
    http_response = (
        "HTTP/1.1 200 OK\r\n"  # Статус ответа 200 OK
        "Content-Type: text/html; charset=UTF-8\r\n"  # Тип содержимого: HTML с UTF-8
        f"Content-Length: {len(html_content.encode('utf-8'))}\r\n"  # Длина содержимого в байтах
        "Connection: close\r\n"  # Закрываем соединение после ответа
        "\r\n"  # Пустая строка, разделяющая заголовки и тело
        + html_content  # Тело ответа: HTML-код
    )

    # Отправляем клиенту HTTP-ответ полностью и закрываем соединение
    client_connection.sendall(http_response.encode("utf-8"))
    client_connection.close()
    print("Server off...")  # Сообщение о закрытии соединения