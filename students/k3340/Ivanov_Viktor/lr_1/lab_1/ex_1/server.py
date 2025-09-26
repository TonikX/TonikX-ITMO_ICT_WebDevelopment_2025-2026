import socket

# параметры сервера
HOST = 'localhost'  # адрес хоста
PORT = 8080         # порт для работы сервера

# создаем UDP сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# привязываем сокет к адресу и порту
server_socket.bind((HOST, PORT))
print(f"UDP сервер запущен на {HOST}:{PORT}...")
print("Ожидание сообщений от клиента...")

while True:
    try:
        # получаем данные от клиента
        data, client_address = server_socket.recvfrom(1024)
        
        # декодируем полученное сообщение
        message = data.decode('utf-8')
        print(f"Получено сообщение от {client_address}: {message}")
        
        # формируем ответ для клиента
        response = "Hello, client"
        
        # отправляем ответ клиенту
        server_socket.sendto(response.encode('utf-8'), client_address)
        print(f"Отправлен ответ клиенту {client_address}: {response}")
        
    except KeyboardInterrupt:
        print("\nСервер остановлен пользователем")
        break
    except Exception as e:
        print(f"Ошибка: {e}")

# закрываем сокет
server_socket.close()
print("Сервер завершил работу")
