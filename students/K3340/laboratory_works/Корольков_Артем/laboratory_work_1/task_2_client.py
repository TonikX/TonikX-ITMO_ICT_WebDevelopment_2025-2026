import socket


def main():
    # Создаем TCP-сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Адрес сервера
    server_address = ('localhost', 12346)

    try:
        # Устанавливаем соединение с сервером
        client_socket.connect(server_address)
        print("Подключение к серверу установлено")

        # Запрашиваем данные у пользователя
        print("Введите параметры трапеции:")
        base_a = input("Основание a: ")
        base_b = input("Основание b: ")
        height = input("Высота h: ")

        # Формируем запрос в формате: a,b,h
        request = f"{base_a},{base_b},{height}"

        # Отправляем запрос серверу
        client_socket.sendall(request.encode('utf-8'))
        print(f"Отправлен запрос: {request}")

        # Получаем ответ от сервера
        response = client_socket.recv(1024).decode('utf-8')
        print(f"Ответ сервера: {response}")

    except ConnectionRefusedError:
        print("Не удалось подключиться к серверу. Убедитесь, что сервер запущен.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        # Закрываем соединение
        client_socket.close()
        print("Соединение закрыто")


if __name__ == "__main__":
    main()