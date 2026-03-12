import socket

# Создаем UDP-сокет для приема и отправки сообщений
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет к локальному адресу и порту 8080
server_socket.bind(('localhost', 8080))
print("UDP сервер запущен на порту 8080...")

while True:
    # Ждем данные от клиента
    client_socket, client_address = server_socket.accept()
    print(f"Подключен клиент {client_address}")

    # Получаем данные от клиента
    data = client_socket.recv(1024)
    message = data.decode()
    print(f"Запрос от клиента {client_address}: {message}")

    try:
        # Преобразуем строку в два числа и вычисляем площадь
        a, h = map(float, message.split())
        area = a * h
        response = f"Площадь параллелограмма = {area}"
    except Exception as e:
        # Если данные некорректные, формируем сообщение об ошибке
        response = f"Ошибка: {e}"

    # Отправляем результат обратно клиенту
    client_socket.send(response.encode())

