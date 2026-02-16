import socket

# Создаем TCP сокет
# AF_INET - используем IPv4
# SOCK_STREAM - указываем TCP протокол
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет к адресу и порту
server.bind(('localhost', 8080))

# Начинаем прослушивание соединений
server.listen(1)
print(f"Сервер запущен на http://localhost:8080")

# Загружаем HTML-страницу из файла
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

while True:
    # Принимаем соединение от клиента
    conn, addr = server.accept()

    # Получаем запрос от клиента
    request = conn.recv(1024).decode('utf-8')

    # Формируем HTTP-ответ
    response = f"""HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: {len(html.encode('utf-8'))}
Connection: close

{html}"""

    # Отправляем ответ клиенту
    conn.sendall(response.encode('utf-8'))

    # Закрываем соединение
    conn.close()