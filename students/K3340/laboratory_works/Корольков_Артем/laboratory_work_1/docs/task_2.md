# Задание 2: TCP-сервер с математической операцией
## Цель
Реализовать TCP-сервер, вычисляющий площадь трапеции по параметрам от клиента.

## Реализация
Сервер: `task_2_server.py` - обрабатывает запросы на порту 12346

Клиент: `task_2_client.py` - отправляет параметры трапеции

## Математическая формула
S = (a + b) * h / 2, где:
a, b - основания трапеции,
h - высота трапеции

## Ключевые особенности
- Использование socket.SOCK_STREAM для TCP
- Установление соединения с помощью connect() и accept()
- Форматированный обмен данными (разделитель - запятая)

## Ход выполнения
### Запуск сервера
```python
    import socket


    def calculate_trapezoid_area(base_a, base_b, height):
    """Вычисляет площадь трапеции по формуле: S = (a + b) * h / 2"""
    try:
        a = float(base_a)
        b = float(base_b)
        h = float(height)
        area = (a + b) * h / 2
        return f"Площадь трапеции с основаниями {a} и {b} и высотой {h} равна: {area:.2f}"
    except ValueError:
        return "Ошибка: Все параметры должны быть числами!"


    def main():
    # Создаем TCP-сокет (SOCK_STREAM)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Привязываем сокет к адресу и порту
    server_address = ('localhost', 12346)
    server_socket.bind(server_address)

    # Начинаем прослушивание входящих подключений
    server_socket.listen(1)
    print("Сервер запущен и ожидает подключений...")

    while True:
        try:
            # Принимаем подключение
            client_socket, client_address = server_socket.accept()
            print(f"Подключился клиент: {client_address}")

            # Получаем данные от клиента
            data = client_socket.recv(1024).decode('utf-8')
            print(f"Получены данные: {data}")

            # Разбираем параметры (ожидаем формат: a,b,h)
            params = data.split(',')
            if len(params) == 3:
                result = calculate_trapezoid_area(params[0], params[1], params[2])
            else:
                result = "Ошибка: Неверный формат данных. Ожидается: основание1,основание2,высота"

            # Отправляем результат клиенту
            client_socket.sendall(result.encode('utf-8'))
            print(f"Отправлен результат: {result}")

            # Закрываем соединение с клиентом
            client_socket.close()

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            if 'client_socket' in locals():
                client_socket.close()


    if __name__ == "__main__":
        main()
```
### Запуск клиента
```python
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
```
## Вывод по заданию 2
Реализовано TCP-взаимодействие для вычисления площади трапеции. Сервер корректно обрабатывает входящие параметры, выполняет расчет и возвращает результат. TCP-протокол обеспечивает надежную доставку данных, что важно для математических вычислений.
