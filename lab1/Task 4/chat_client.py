import socket
import threading

HOST = "localhost"  # Адрес сервера
PORT = 8080         # Порт сервера

# Функция для получения сообщений от сервера в отдельном потоке
def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)  # Получаем данные от сервера
            if not data:             # Если сервер закрыл соединение
                break
            print(data.decode("utf-8"))  # Выводим полученное сообщение
        except:
            break

# Создаем TCP-сокет и подключаемся к серверу
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

# Запускаем отдельный поток для получения сообщений от сервера
threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

try:
    while True:
        # Вводим сообщение и отправляем на сервер
        msg = input()
        sock.sendall(msg.encode("utf-8"))
except KeyboardInterrupt:
    # Завершаем работу при Ctrl+C
    print("\nВыход...")
finally:
    # Закрываем соединение
    sock.close()
