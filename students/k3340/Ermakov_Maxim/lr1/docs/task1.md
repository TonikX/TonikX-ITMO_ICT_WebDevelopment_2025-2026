# Задание 1

Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.

**Требования:**
- Обязательно использовать библиотеку `socket`.
- Реализовать с помощью протокола **UDP**.

---

## Решение

### Сервер
```python
import socket

# На каком адресе и порту слушаем
SERVER_HOST = "127.0.0.1"  
SERVER_PORT = 8080        

# Создаём UDP-сокет: AF_INET (IPv4), SOCK_DGRAM (UDP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Привязываем сокет к адресу/порту, чтобы принимать датаграммы
server_socket.bind((SERVER_HOST, SERVER_PORT))
print(f"UDP-сервер запущен на {SERVER_HOST}:{SERVER_PORT}")
print("Ожидаю сообщения от клиента... (Ctrl+C для выхода)\n")

try:
    while True:
        # recvfrom возвращает (данные, адрес_клиента)
        data, client_addr = server_socket.recvfrom(1024)  # до 1024 байт
        message = data.decode("utf-8", errors="ignore")
        print(f"Получено от {client_addr}: {message}")

        # Формируем ответ
        reply = "Hello, client"
        server_socket.sendto(reply.encode("utf-8"), client_addr)
        print(f"Отправлен ответ клиенту {client_addr}: {reply}\n")

except KeyboardInterrupt:
    print("\nСервер остановлен пользователем.")
finally:
    server_socket.close()
```

### Клиент
```python
import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9091

# Создаём UDP-сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    # Сообщение серверу
    msg = "Hello, server"
    client_socket.sendto(msg.encode("utf-8"), (SERVER_HOST, SERVER_PORT))
    print(f"Отправлено на сервер {SERVER_HOST}:{SERVER_PORT}: {msg}")

    # Ждём ответ
    data, server_addr = client_socket.recvfrom(1024)
    reply = data.decode("utf-8", errors="ignore")
    print(f"Ответ от сервера {server_addr}: {reply}")

except socket.timeout:
    print("Не дождались ответа от сервера (timeout).")
finally:
    client_socket.close()
```

---

## Пояснение

Создаём UDP сокет на сервере, используя адрес `127.0.0.1` и порт `9090`, после чего в бесконечном цикле пытаемся прочитать данные от
клиента и напечатать их, а затем отправить сообщение `Hello, client` клиенту.

Клиент создает UDP сокет и без установки соединения отправляет данные на `127.0.0.1:9090`. Затем читает ответ от сервера и закрывает сокет.
