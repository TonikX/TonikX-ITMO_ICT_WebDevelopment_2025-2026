# Задача 2

## Цель
Реализовать клиентскую и серверную часть приложения с использованием библиотеки **socket** и протокола **TCP**.  
Клиент запрашивает выполнение математической операции (в данном случае — **теорема Пифагора**), сервер обрабатывает данные и возвращает результат клиенту.

## Выполнение
В ходе выполнения были реализованы клиент и сервер, где:
- **Клиент** подключается к серверу по TCP, вводит 2 числа через запятую и отправляет их.  
- **Сервер** принимает числа, вычисляет решение теорему Пифагора и возвращает результат клиенту.  
- Также на сервере обработан случай, с неправильным вводом.

### Клиент
```python
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
```


### Сервер
```python
import socket
import math


def handle_pythagoras(data):
    """Обработка теоремы Пифагора"""
    try:
        # Разбираем данные: катет1, катет2
        parts = data.split(',')
        if len(parts) != 2:
            return "Ошибка: необходимо ввести два катета через запятую"

        a = float(parts[0])
        b = float(parts[1])

        if a <= 0 or b <= 0:
            return "Ошибка: катеты должны быть положительными числами"

        # Вычисляем гипотенузу
        c = math.sqrt(a ** 2 + b ** 2)

        return f"Гипотенуза треугольника с катетами {a} и {b} = {c:.2f}"

    except ValueError:
        return "Ошибка: введите числа в правильном формате"
    except Exception as e:
        return f"Ошибка при вычислении: {e}"


def start_server():
    """Запуск TCP сервера"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind(('localhost', 8080))
        server_socket.listen(5)
        print("Сервер запущен на localhost:8080")
        print("Ожидание подключений...")

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Подключен клиент: {client_address}")

            try:
                # Получаем данные от клиента
                data = client_socket.recv(1024).decode('utf-8')
                print(f"Получены данные: {data}")

                # Обрабатываем запрос
                result = handle_pythagoras(data)

                # Отправляем результат клиенту
                client_socket.send(result.encode('utf-8'))
                print(f"Отправлен результат: {result}")

            except Exception as e:
                error_msg = f"Ошибка обработки запроса: {e}"
                client_socket.send(error_msg.encode('utf-8'))
            finally:
                client_socket.close()
                print(f"Соединение с {client_address} закрыто\n")

    except KeyboardInterrupt:
        print("\nСервер остановлен")
    except Exception as e:
        print(f"Ошибка сервера: {e}")
    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server()
```

## Результат

Варианты ответа клиенту:

![](assets/task2client0.png)
![](assets/task2client1.png)

Работа сервера:

![](assets/task2server.png)

## Вывод

Была реализована клиент-серверная архитектура с использованием TCP-сокетов для решения теоремы Пифагора.