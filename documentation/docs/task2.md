# Задание 2

Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции (вариант 4 — **площадь параллелограмма**). Параметры вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат.

**Требования:**
- Обязательно использовать библиотеку `socket`.
- Реализовать с помощью протокола **TCP**.

---

## Решение

### Сервер 
```python
import socket

HOST = "127.0.0.1"  
PORT = 9091          

#  создаём TCP-сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# привязываем к адресу и порту
server_socket.bind((HOST, PORT))

# начинаем слушать входящие подключения
server_socket.listen(1)
print(f"Сервер запущен на {HOST}:{PORT}")
print("Жду подключения клиента... \n")

try:
    while True:
        #  принимаем одно подключение
        conn, addr = server_socket.accept()
        print(f"Клиент подключился: {addr}")

        # читаем строку с двумя числами: "<a> <h>"
        data = conn.recv(1024)
        text = data.decode("utf-8").strip()
        print(f"Получено: {text!r}")

        #  пробуем распарсить два числа
        try:
            a_str, h_str = text.split()
            # поддержим ввод с запятой
            a = float(a_str.replace(",", "."))
            h = float(h_str.replace(",", "."))
            area = a * h
            reply = f"{area:.6f}"  # только число
        except Exception:
            reply = "Ошибка: введите два числа через пробел, например: 7.5 3"

        # отправляем ответ и закрываем соединение
        conn.sendall(reply.encode("utf-8"))
        print(f"Отправлено: {reply}\n")
        conn.close()

except KeyboardInterrupt:
    print("\nСервер остановлен.")
finally:
    server_socket.close()
```

### Клиент
```python
import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9091

# Просим пользователя ввести данные с клавиатуры
print("Введите параметры параллелограмма")
a = input("Введите основание a: ").strip()
h = input("Введите высоту h: ").strip()

# Формируем запрос
request = f"{a} {h}"

# Создаём TCP-сокет, подключаемся к серверу и отправляем запрос
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    client_socket.sendall(request.encode("utf-8"))

    #  Получаем ответ
    data = client_socket.recv(1024)
    reply = data.decode("utf-8").strip()

    print(f"Ответ от сервера: {reply}")

except ConnectionRefusedError:
    print("Не удалось подключиться к серверу.")
finally:
    client_socket.close()
```

---

## Пояснение

- Клиент вводит **основание** и **высоту**, отправляет их одной строкой `<a> <h>`.
- Сервер парсит два числа, считает `S = a * h` и возвращает ответ строкой.
- TCP обеспечивает надёжную доставку и порядок сообщений.
