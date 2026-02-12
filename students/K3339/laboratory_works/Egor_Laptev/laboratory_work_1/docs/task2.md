
## Задание 2:
Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

### Используемые технологии:
- Python socket
- Протокол TCP

### Файлы:

**client.py**
```python
import socket

HOST = 'localhost'
PORT = 8080

base = float(input("Основание параллелограмма: "))
height = float(input("Высота параллелограмма: "))

params = [base, height]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
message = ','.join(map(str, params))
sock.send(message.encode())
data = sock.recv(1024)
sock.close()

print("Площадь параллелограмма:", data.decode())

```

**server.py**
```python
import socket


def parallelogram_area(base, height):
    return base * height


HOST = 'localhost'
PORT = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(1)
print("[TCP] Server is running on port {}".format(PORT))

while True:
    conn, addr = sock.accept()
    print(f"Подключен клиент: {addr}")
    try:
        data = conn.recv(1024).decode()
        if not data:
            continue

        params = data.split(',')

        base, height = map(float, params)
        result = parallelogram_area(base, height)
        conn.send(str(result).encode())
    except Exception as e:
        conn.send(f"Ошибка: {e}".encode())
    finally:
        conn.close()

```

### Результат работы:
Сервер:
```
[TCP] Server is running on port 8080
Подключен клиент: ('127.0.0.1', 53214)
```
Клиент:

```
Основание параллелограмма: 5
Высота параллелограмма: 3
Площадь параллелограмма: 15.0
```