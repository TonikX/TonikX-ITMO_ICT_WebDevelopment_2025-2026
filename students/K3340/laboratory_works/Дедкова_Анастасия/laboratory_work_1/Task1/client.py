import socket

HOST = 'localhost'  # Адрес сервера
PORT = 9090         # Порт сервера

# Создаем UDP сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    # Сообщение для сервера
    message = "Hello, server"
    
    # Отправляем сообщение серверу
    print(f"Отправляю сообщение серверу: {message}")
    client_socket.sendto(message.encode('utf-8'), (HOST, PORT))
    
    # Получаем ответ от сервера
    print("Ожидание ответа от сервера...")
    data, server_address = client_socket.recvfrom(1024)
    
    # Декодируем полученный ответ
    response = data.decode('utf-8')
    print(f"Получен ответ от сервера {server_address}: {response}")
    
except Exception as e:
    print(f"Ошибка: {e}")
    
finally:
    # Закрываем сокет
    client_socket.close()
    print("Клиент завершил работу")
