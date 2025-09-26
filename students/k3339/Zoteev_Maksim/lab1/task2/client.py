import socket

# Создаем TCP сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Адрес сервера
server_address = ('localhost', 12346)

try:
    # Подключаемся к серверу
    print("Подключение к серверу...")
    client_socket.connect(server_address)
    print("Соединение установлено!")
    
    # Запрашиваем данные у пользователя
    print("\n=== Вычисление площади параллелограмма ===")
    print("Формула: Площадь = основание × высота")
    
    base = input("Введите основание параллелограмма: ")
    height = input("Введите высоту параллелограмма: ")
    
    # Формируем сообщение
    message = f"{base},{height}"
    print(f"Отправляем данные серверу: {message}")
    
    # Отправляем данные серверу
    client_socket.send(message.encode('utf-8'))
    
    # Получаем результат от сервера
    response_data = client_socket.recv(1024)
    result = response_data.decode('utf-8')
    
    print(f"\nОтвет сервера: {result}")
    
except ConnectionRefusedError:
    print("Ошибка: не удается подключиться к серверу. Убедитесь, что сервер запущен.")
except Exception as e:
    print(f"Ошибка: {e}")

finally:
    # Закрываем соединение
    client_socket.close()
    print("Соединение закрыто.")
