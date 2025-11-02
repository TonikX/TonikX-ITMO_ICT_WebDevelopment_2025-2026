import socket

# Создаем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4, TCP
# Привязываем сокет к адресу и порту
server_socket.bind(('localhost', 8080))
# Слушаем входящие соединения
server_socket.listen(1)

print("Сервер запущен на порту 8080...")

while True:
    # Принимаем соединение от клиента
    client_connection, client_address = server_socket.accept()
    print(f'Подключение от {client_address}')

    # Получаем сообщение от клиента
    data = client_connection.recv(1024).decode()
    print(f'Запрос от клиента: {data}')

    # Разбираем данные и вычисляем площадь трапеции
    try:
        base1, base2, height = map(float, data.split(','))
        area = (base1 + base2) * height / 2
        response = f'Площадь трапеции: {area:.2f}'
    except:
        response = 'Ошибка: неверный формат данных'

    # Отправляем ответ клиенту
    client_connection.sendall(response.encode())

    # Закрываем соединение
    client_connection.close()