import socket
import threading


def receive_messages(client_socket): # Функция для получения сообщений от сервера
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print("\nСоединение с сервером разорвано.")
                break
            print(f"\n{message}")
            print("> ", end="", flush=True)
    except:
        print("\nОшибка соединения с сервером.")


def start_client(host='localhost', port=1234):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port)) # Подключаемся к серверу
        nickname = input("Введите ваш никнейм: ")# Запрашиваем никнейм у пользователя
        # Отправляем никнейм серверу как первое сообщение
        client_socket.send(f"{nickname} присоединился к чату".encode('utf-8'))
        print(f"\nДобро пожаловать в чат, {nickname}!")
        print("Для выхода введите 'exit' или нажмите Ctrl+C")

        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))# Запускаем поток для получения сообщений
        receive_thread.daemon = True
        receive_thread.start()

        while True: # Основной цикл отправки сообщений
            message = input("You: ")
            if message.lower() == 'exit':
                break

            formatted_message = f"{nickname}: {message}" # Форматируем сообщение с ником
            client_socket.send(formatted_message.encode())

    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        client_socket.close()
        print("Выход из чата.")

start_client()