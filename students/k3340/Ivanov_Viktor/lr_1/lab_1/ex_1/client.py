import socket

# параметры сервера
HOST = 'localhost'  # адрес сервера
PORT = 8080         # порт сервера

# создаем UDP сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    # сообщение для отправки серверу
    message = "Hello, server"
    
    # отправляем сообщение серверу
    print(f"Отправляю сообщение серверу: {message}")
    client_socket.sendto(message.encode('utf-8'), (HOST, PORT))
    
    # получаем ответ от сервера
    print("Ожидание ответа от сервера...")
    data, server_address = client_socket.recvfrom(1024)
    
    # декодируем полученный ответ
    response = data.decode('utf-8')
    print(f"Получен ответ от сервера {server_address}: {response}")
    
except Exception as e:
    print(f"Ошибка: {e}")
    
finally:
    # закрываем сокет
    client_socket.close()
    print("Клиент завершил работу")
