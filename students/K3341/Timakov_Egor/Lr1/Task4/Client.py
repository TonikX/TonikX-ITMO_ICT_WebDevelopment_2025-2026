import socket
import threading
import sys

# Настройки сервера для подключения
HOST = '127.0.0.1'
PORT = 55555


def receive_messages(client_socket):
    """Функция, запускаемая в отдельном потоке для непрерывного получения сообщений."""
    while True:
        try:
            # Получаем сообщение
            message = client_socket.recv(1024).decode('utf-8')

            if not message:
                # Если нет сообщения, сервер, вероятно, отключился
                print("\n[ОТКЛЮЧЕНИЕ] Сервер недоступен. Нажмите Enter для выхода.")
                client_socket.close()
                sys.exit()

            # Выводим полученное сообщение
            print(f"\n{message}")
        except:
            # Обработка ошибки сокета при отключении
            break


def start_client():
    """Инициализация клиента, подключение и обработка отправки сообщений."""

    # Запрос никнейма
    nickname = input("Введите ваш никнейм: ")

    #  Создание и подключение сокета
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
        print(f"Подключено к чату как {nickname}. Начните печатать сообщения...")
    except ConnectionRefusedError:
        print(f"Ошибка: Не удалось подключиться к серверу {HOST}:{PORT}. Убедитесь, что сервер запущен.")
        sys.exit()

    #  Отправка никнейма серверу (должно быть первым сообщением)
    client.send(nickname.encode('utf-8'))

    #  Запуск потока для получения сообщений
    # Поток будет работать независимо от основного потока ввода
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.daemon = True  # Поток автоматически завершится, когда завершится основная программа
    receive_thread.start()

    # 4. Основной цикл для отправки сообщений
    while True:
        try:
            # Чтение ввода пользователя (блокирует основной поток)
            message_to_send = input("")

            # Проверка на команду выхода
            if message_to_send.lower() in ('/quit', '/exit'):
                print("Отключение от чата...")
                client.close()
                break

            # Отправка сообщения серверу
            client.send(message_to_send.encode('utf-8'))

        except EOFError:
            # Обработка Ctrl+D
            print("Отключение от чата.")
            client.close()
            break
        except Exception as e:
            print(f"Произошла ошибка при отправке: {e}")
            client.close()
            break


if __name__ == "__main__":
    start_client()