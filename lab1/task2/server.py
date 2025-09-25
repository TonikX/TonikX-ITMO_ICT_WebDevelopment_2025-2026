import socket

# Создаем TCP сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Указываем адрес и порт для сервера
server_address = ('localhost', 12346)
server_socket.bind(server_address)

# Начинаем прослушивание (максимум 1 подключение в очереди)
server_socket.listen(1)

print("TCP сервер запущен на", server_address)
print("Ожидание подключений...")

while True:
    # Ждем подключения клиента
    client_socket, client_address = server_socket.accept()
    print(f"Подключился клиент: {client_address}")
    
    try:
        # Получаем данные от клиента
        data = client_socket.recv(1024)
        message = data.decode('utf-8')
        print(f"Получены данные: {message}")
        
        # Парсим данные (ожидаем формат "основание,высота")
        try:
            base, height = map(float, message.split(','))
            
            # Вычисляем площадь параллелограмма
            area = base * height
            result = f"Площадь параллелограмма: {area}"
            print(f"Результат вычисления: {result}")
            
        except ValueError:
            result = "Ошибка: неверный формат данных. Используйте: основание,высота"
            print("Ошибка в данных от клиента")
        
        # Отправляем результат клиенту
        client_socket.send(result.encode('utf-8'))
        
    except Exception as e:
        print(f"Ошибка при обработке клиента: {e}")
    
    finally:
        # Закрываем соединение с клиентом
        client_socket.close()
        print("Соединение с клиентом закрыто\n")
