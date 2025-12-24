# Реализация клиентской и серверной части приложения (UDP)

## Условие задания  
Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.  

**Требования:**  
- Использовать библиотеку `socket`.  
- Реализовать через протокол UDP.  

## Алгоритм решения  
- Создать серверный сокет UDP, привязать его к адресу (`localhost`, порт `8080`).  
- Сервер в бесконечном цикле принимает сообщения от клиента и выводит их на экран.  
- После получения сообщения сервер отправляет ответ клиенту.  
- Клиент создаёт UDP-сокет, отправляет сообщение серверу.  
- Клиент получает ответ и выводит его на экран.  
- После получения ответа клиент закрывает сокет.  

## Код сервера
```python
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_socket.bind(('localhost', 8080))

print('Сервер запущен и ждёт сообщений...')

while True:
    data, client_address = server_socket.recvfrom(1024)
    print(f'От клиента ({client_address}): {data.decode()}')

    response = 'Hello, client'
    server_socket.sendto(response.encode(), client_address)
```

## Код клиента
```python
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message = 'Hello, server'
client_socket.sendto(message.encode(), ('localhost', 8080))

data, server_address = client_socket.recvfrom(1024)
print(f'Ответ от сервера: {data.decode()}')

client_socket.close()
```

## Результат работы
```python
Сервер запущен и ждёт сообщений...
От клиента (('127.0.0.1', 58409)): Hello, server

Ответ от сервера: Hello, client
```