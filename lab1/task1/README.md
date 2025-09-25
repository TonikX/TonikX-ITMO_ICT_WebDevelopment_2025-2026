# Лабораторная работа 1, Задание 1: UDP клиент-сервер

## Описание
Простое приложение клиент-сервер, использующее протокол **UDP**.
Клиент отправляет сообщение "Hello, server", сервер отвечает "Hello, client".

## Файлы
- `server.py` - серверная часть
- `client.py` - клиентская часть

## Как запустить

### 1. Запустите сервер:
```bash
python3 server.py
```

### 2. В другом терминале запустите клиент:
```bash
python3 client.py
```

## Результат
- На сервере появится сообщение о получении "Hello, server"
- На клиенте появится сообщение о получении "Hello, client"

## Технические детали
- **Протокол:** UDP (User Datagram Protocol)
- **Порт сервера:** 12345
- **Адрес:** localhost (127.0.0.1)
- **Тип сокета:** `SOCK_DGRAM`

## Требования
- Python 3.x
- Библиотека `socket` (входит в стандартную библиотеку Python)

## Особенности UDP
- Без установления соединения
- Передача отдельными пакетами (датаграммами)
- Быстрая передача, но без гарантий доставки

## Примеры кода

### Сервер (server.py)
```python
import socket

# Создание UDP сокета
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 12345)
server_socket.bind(server_address)

while True:
    # Получение данных от клиента
    data, client_address = server_socket.recvfrom(1024)
    message = data.decode('utf-8')
    
    # Отправка ответа
    response = "Hello, client"
    server_socket.sendto(response.encode('utf-8'), client_address)
```

### Клиент (client.py)
```python
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 12345)

# Отправка сообщения
message = "Hello, server"
client_socket.sendto(message.encode('utf-8'), server_address)

# Получение ответа
response_data, server_addr = client_socket.recvfrom(1024)
response = response_data.decode('utf-8')
client_socket.close()
```

## Алгоритм работы

### Сервер:
1. Создание UDP сокета с `SOCK_DGRAM`
2. Привязка к адресу и порту (`bind()`)
3. Бесконечный цикл ожидания сообщений (`recvfrom()`)
4. Декодирование полученных данных
5. Отправка ответа клиенту (`sendto()`)

### Клиент:
1. Создание UDP сокета
2. Отправка сообщения серверу (`sendto()`)
3. Ожидание ответа (`recvfrom()`)
4. Декодирование и отображение ответа
5. Закрытие сокета
