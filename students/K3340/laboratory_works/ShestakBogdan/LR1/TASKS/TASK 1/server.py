import socket  # Импортируем модуль socket для работы с сетевыми соединениями

sock_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
# Создаём UDP-сокет (SOCK_DGRAM) для протокола IPv4 (AF_INET)

sock_server.bind(('localhost', 8080))  
# Привязываем сокет к адресу 'localhost' и порту 8080, чтобы сервер мог принимать данные

while True:  # Бесконечный цикл для постоянного прослушивания входящих сообщений
    request, address = sock_server.recvfrom(1024)  
    # Получаем сообщение от клиента и его адрес; буфер ограничен 1024 байтами
    print(f'Client {address}: {request.decode()}')  
    # Декодируем байты в строку и выводим сообщение клиента в консоль

    msg = 'Hello, client'  # Создаём ответное сообщение
    sock_server.sendto(msg.encode(), address)  
    # Кодируем строку в байты и отправляем обратно клиенту по его адресу