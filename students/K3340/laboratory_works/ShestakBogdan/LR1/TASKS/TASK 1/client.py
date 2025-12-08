import socket  # Импортируем модуль для работы с сетевыми сокетами

sock_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
# Создаём UDP-сокет (SOCK_DGRAM) для IPv4 (AF_INET)

msg = 'Hello, server'  # Сообщение, которое будем отправлять серверу

sock_client.sendto(msg.encode(), ("localhost", 8080))  
# Отправляем сообщение серверу по адресу localhost и порту 8080, кодируя строку в байты

response, address = sock_client.recvfrom(1024)  
# Получаем ответ от сервера (максимум 1024 байта) и адрес отправителя

print(f'Server {address}: {response.decode()}')  
# Декодируем байты обратно в строку и выводим адрес сервера и его ответ

