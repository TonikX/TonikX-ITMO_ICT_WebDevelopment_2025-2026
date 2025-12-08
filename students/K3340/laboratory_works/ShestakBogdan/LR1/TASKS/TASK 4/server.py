import socket      # Модуль для работы с сетевыми сокетами
import threading   # Модуль для работы с потоками (чтобы обрабатывать клиентов параллельно)

users = []          # Список подключенных клиентов
lock = threading.Lock()  
# Блокировка для безопасного доступа к общему списку users из разных потоков

def process_user(client_connection):  
    # Функция для обработки сообщений одного клиента
    global users  
    while True:  
        msg = client_connection.recv(1024)  
        # Получаем сообщение от клиента (до 1024 байт)
        with lock:  
            # Закрываем доступ к списку users на время отправки сообщений
            for user in users:  
                if user != client_connection:  
                    user.sendall(msg)  
                    # Отправляем сообщение всем клиентам, кроме отправителя

# Создаем TCP-сокет для сервера
sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock_server.bind(('localhost', 8080))  
# Привязываем сокет к адресу localhost и порту 8080

sock_server.listen(5)  
# Начинаем слушать соединения, с очередью до 5 подключений
print("Chat started...")  

while True:  # Основной цикл для принятия новых клиентов
    client_connection, client_address = sock_server.accept()  
    # Принимаем подключение клиента
    print(f'{client_address} Connected')  

    with lock:  
        users.append(client_connection)  
        # Добавляем нового клиента в список пользователей безопасно

    thr = threading.Thread(target=process_user, args=(client_connection,))  
    thr.start()  
    # Создаем новый поток для обработки сообщений этого клиента
