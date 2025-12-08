import socket

# Параметры сервера
HOST = 'localhost'  # Адрес хоста
PORT = 9090         # Порт для работы сервера

# Создаем UDP сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Привязываем сокет к адресу и порту
server_socket.bind((HOST, PORT))
print(f"UDP сервер запущен на {HOST}:{PORT}...")
print("Ожидание сообщений от клиента...")

while True:
    try:
        # Получаем данные от клиента
        data, client_address = server_socket.recvfrom(1024)
        
        # Декодируем полученное сообщение
        message = data.decode('utf-8')
        print(f"Получено сообщение от {client_address}: {message}")
        
        # Ответ для клиента
        response = "Hello, client"
        
        # Отправляем ответ клиенту
        server_socket.sendto(response.encode('utf-8'), client_address)
        print(f"Отправлен ответ клиенту {client_address}: {response}")
        
    except KeyboardInterrupt:
        print("\nСервер остановлен пользователем")
        break
    except Exception as e:
        print(f"Ошибка: {e}")

# Закрываем сокет
server_socket.close()
print("Сервер завершил работу")
