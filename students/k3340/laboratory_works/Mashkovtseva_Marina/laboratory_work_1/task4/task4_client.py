import socket
import threading

# Настройки сервера
HOST = 'localhost'
PORT = 8080

# Создаем TCP-сокет и подключаемся к серверу
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print("Подключение к чату установлено!")


def receive_messages():
    """Получает сообщения от сервера в отдельном потоке"""
    while True:
        try:
            # Получаем сообщение от сервера
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            # Ошибка при получении = разрыв соединения
            print("Соединение разорвано!")
            break


# Поток для получения сообщений от сервера
receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True # Фоновый режим (завершится с программой)
receive_thread.start() # Запускаем прием сообщений

# Отправляем сообщения на сервер
while True:
    message = input()

    if message.lower() == 'выход':
        break

    # Отправляем сообщение на сервер
    try:
        client_socket.send(message.encode('utf-8'))
    except:
        print("Не удалось отправить сообщение!")
        break

client_socket.close()