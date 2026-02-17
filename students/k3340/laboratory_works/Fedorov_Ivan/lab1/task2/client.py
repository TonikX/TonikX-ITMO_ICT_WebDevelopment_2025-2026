import socket


def show_menu():
    """Показывает меню операций"""
    print("\n" + "=" * 50)
    print("МАТЕМАТИЧЕСКИЕ ОПЕРАЦИИ")
    print("=" * 50)
    print("Теорема Пифагора: вычисление гипотенузы по двум катетам")
    print("Формат ввода: два катета через запятую (например: 3,4)")
    print("Для выхода введите 'exit'")
    print("=" * 50)


def get_user_input():
    """Получает ввод от пользователя"""
    while True:
        user_input = input("\nВведите катеты через запятую: ").strip()

        if user_input.lower() == 'exit':
            return None

        if ',' not in user_input:
            print("Ошибка: используйте запятую для разделения катетов")
            continue

        return user_input


def connect_to_server(data):
    """Подключается к серверу и отправляет данные"""
    try:
        # Создаем TCP сокет
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(10)  # Таймаут 10 секунд

        # Подключаемся к серверу
        client_socket.connect(('localhost', 8080))

        # Отправляем данные
        client_socket.send(data.encode('utf-8'))

        # Получаем ответ
        response = client_socket.recv(1024).decode('utf-8')

        return response

    except socket.timeout:
        return "Ошибка: превышено время ожидания ответа от сервера"
    except ConnectionRefusedError:
        return "Ошибка: не удалось подключиться к серверу. Убедитесь, что сервер запущен."
    except Exception as e:
        return f"Ошибка соединения: {e}"
    finally:
        client_socket.close()


def main():
    """Основная функция клиента"""
    print("Клиент теоремы Пифагора запущен")

    while True:
        show_menu()
        user_input = get_user_input()

        if user_input is None:
            print("Завершение работы...")
            break

        if not user_input:
            continue

        print("Отправка данных на сервер...")
        result = connect_to_server(user_input)

        print("\n" + "=" * 50)
        print("РЕЗУЛЬТАТ:")
        print(result)
        print("=" * 50)


if __name__ == "__main__":
    main()