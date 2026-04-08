import socket
import threading

# Функция для получения сообщений от сервера и их отображения
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')  # Получаем сообщение от сервера
            if message:
                print(message)  # Выводим сообщение на экран с указанием имени отправителя
        except:
            print("Connection closed by server.")  # Сообщаем, если соединение закрыто сервером
            break  # Выходим из цикла при ошибке

# Функция для отправки сообщений на сервер
def send_messages(client_socket):
    while True:
        try:
            message = input()  # Получаем ввод пользователя
            if message.lower() == "exit":  # Если пользователь ввел "exit"
                print("Disconnecting from server...")  # Логируем отключение
                client_socket.close()  # Закрываем сокет
                break  # Выходим из цикла
            client_socket.send(message.encode('utf-8'))  # Отправляем сообщение серверу
        except:
            break  # Выходим из цикла при ошибке

# Основная функция клиента
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Создаем TCP сокет
    client_socket.connect(('localhost', 5555))  # Подключаемся к серверу
    print("Connected to server. Type messages and press Enter. Type 'exit' to quit.")

    # Создаем отдельные потоки для получения и отправки сообщений
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()
    threading.Thread(target=send_messages, args=(client_socket,), daemon=True).start()

    # Главный цикл предотвращает завершение программы, пока подключение активно
    while True:
        try:
            if client_socket.fileno() == -1:  # Проверка, закрыт ли сокет
                break
        except:
            break  # Выходим из цикла при ошибке

# Запуск клиента
start_client()
