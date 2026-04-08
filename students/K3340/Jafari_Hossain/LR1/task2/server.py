import socket

SERVER_HOST = "127.0.0.1"   # адрес сервера (локальный компьютер)
SERVER_PORT = 12345         # порт, на котором будет работать сервер

# Создаём TCP/IP сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет к адресу и порту
server_socket.bind((SERVER_HOST, SERVER_PORT))

# Запускаем "прослушивание" порта (максимум 1 клиент в очереди)
server_socket.listen(1)
print(f"TCP сервер запущен на {SERVER_HOST}:{SERVER_PORT}")

while True:
    # Ожидаем подключения клиента
    client_socket, client_addr = server_socket.accept()
    print(f"Подключился клиент: {client_addr}")

    try:
        print("Начинаем обработку данных...")
        # Получаем строку с коэффициентами (например: "1,2,3")
        req = client_socket.recv(1024).decode()
        operands = req.split(",")   # разделяем строку по запятым
        a = float(operands[0])      # первый коэффициент
        b = float(operands[1])      # второй коэффициент
        c = float(operands[2])      # третий коэффициент

        # Печатаем для отладки
        print(f"Получены коэффициенты: a = {a}, b = {b}, c = {c}")
    except ValueError:
        # Если пришли некорректные данные
        result = "Ошибка: неверный ввод коэффициентов."
        client_socket.send(result.encode())
        client_socket.close()
        continue

    # Считаем дискриминант
    discriminant = b**2 - 4 * a * c
    print(f"Дискриминант: {discriminant}")

    # Определяем корни по дискриминанту
    if discriminant > 0:
        root1 = (-b + discriminant**0.5) / (2 * a)
        root2 = (-b - discriminant**0.5) / (2 * a)
        result = f"Два корня: x1 = {root1}, x2 = {root2}"
    elif discriminant == 0:
        root = -b / (2 * a)
        result = f"Один корень: x = {root}"
    else:
        result = "Нет действительных корней."

    # Отправляем результат клиенту
    client_socket.send(result.encode())

    # Закрываем соединение с клиентом
    client_socket.close()
