# Задание 1:

---
Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.

### Требования:

Обязательно использовать библиотеку socket.
Реализовать с помощью протокола UDP.

### Выполнение:

#### server.py
Импортируем библиотеку socket, для хоста выбираем локальное устройство,
то есть '127.0.0.1' или же 'localhost'. Для порта берем любой, не считая зарезервированных,
я взяла 9090.

Создаем объект класса сокет, а затем связываем его с нужными нам портом и хостом:
```python
sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))
sock.settimeout(1.0)
```

Далее создаем переменную для хранения переменной с сообщением приветствия клиента и начинаем блок кода,
отвечающий за прослушивание клиентов на сокете:
```python
try:
    while True:
        try:
            data, addr = sock.recvfrom(1024)
        except socket.timeout:
            continue
        if not data:
            break
        print(data.decode('utf-8'))
        sock.sendto(response.encode('utf-8'), addr)
except KeyboardInterrupt:
    print('\nserver stopped')
finally:
    sock.close()
```

Получив адрес подкючившегося клиента, отправляем ему сообщение. 

#### client.py

```python
import socket

UDP_IP = '127.0.0.1'
UDP_PORT = 9090
sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
addr = (UDP_IP, UDP_PORT)
message = 'Hello, server!'
sock.sendto(message.encode('utf-8'), addr)

data, server = sock.recvfrom(1024)
print(data.decode('utf-8'))
sock.close()
```

На клиенте подключаемся к сокету, который прослушивает сервер и получаем долгжданное сообщение и выводим его в консоль:

![img.png](img.png)

А на адрес сервера отправляем ответное приветственное сообщение, которое он успешно получает:

![img_1.png](img_1.png)