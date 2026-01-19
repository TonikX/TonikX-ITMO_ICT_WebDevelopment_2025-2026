import socket

def trapezoid_product(a, b, height):
    return ((a + b)/ 2) * height

# Параметры сервера
HOST = 'localhost'  # Адрес хоста (localhost для локальных соединений)
PORT = 8080         # Порт, на котором будет работать сервер

# Создаем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет к адресу и порту
server_socket.bind((HOST, PORT))

# Начинаем слушать входящие соединения
server_socket.listen(5)
print(f"сервер запущен на {HOST}:{PORT}...")

while True:
    # Принимаем соединение от клиента
    client_connection, client_address = server_socket.accept()
    print(f'Подключение от {client_address}')

    first_request = '''
    Введите длины оснований и высоты через пробел без запятой в формате <a, b, h>, где a, b - длины оснований, h - высота
    '''

    # Отправляем ответ клиенту
    client_connection.sendall(first_request.encode('utf-8'))

    # Получаем запрос от клиента
    data_request = client_connection.recv(1024).decode('utf-8')
    print(f'Полученные данные:\n{data_request}')

    try:
        res = trapezoid_product(*list(map(float, data_request.split())))
    except ValueError:
        client_connection.sendall("Неверный формат входных данных. Подключитесь повторно и попробуйте снова".encode('utf-8'))
        client_connection.close()
        continue

    # Отправляем ответ клиенту
    client_connection.sendall(str(res).encode('utf-8'))

    client_connection.close()