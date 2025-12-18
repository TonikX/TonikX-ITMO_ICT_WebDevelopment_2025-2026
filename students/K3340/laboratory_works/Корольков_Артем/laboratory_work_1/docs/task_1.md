# Задание 1: UDP-клиент и сервер

## Цель
Реализовать клиент-серверное приложение, использующее протокол UDP для обмена сообщениями.

## Реализация

### Сервер (`task_1_server.py`)
Сервер ожидает UDP-сообщения на порту 12345. При получении сообщения выводит его и отправляет ответ "Hello, client".
```python
import socket

# Создаем UDP-сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Привязываем сокет к адресу и порту
server_address = ('localhost', 12345)
server_socket.bind(server_address)

print("Сервер запущен и ожидает сообщений...")

while True:
# Получаем данные и адрес клиента
data, client_address = server_socket.recvfrom(1024)
print(f"Получено сообщение от {client_address}: {data.decode('utf-8')}")

# Формируем ответ
response = "Hello, client"
server_socket.sendto(response.encode('utf-8'), client_address)
print(f"Отправлен ответ: {response}")
```

### Клиент (`task_1_client.py`)
```python
import socket

# Создаем UDP-сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Адрес сервера
server_address = ('localhost', 12345)

# Сообщение для отправки
message = "Hello, server"
client_socket.sendto(message.encode('utf-8'), server_address)
print(f"Отправлено сообщение серверу: {message}")

# Получаем ответ от сервера
data, _ = client_socket.recvfrom(1024)
print(f"Получен ответ от сервера: {data.decode('utf-8')}")

# Закрываем сокет
client_socket.close()
```
## Вывод по заданию 1
Успешно реализовано UDP-взаимодействие между клиентом и сервером. Сервер корректно принимает сообщение от клиента и отправляет ответ. Использован протокол UDP с датаграммами, что обеспечивает простоту реализации для задач, не требующих гарантированной доставки.
