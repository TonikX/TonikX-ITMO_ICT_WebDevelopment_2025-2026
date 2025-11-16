# Задание 1

**Условие:**  
Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.  

**Требования:**
- Использовать библиотеку `socket`.
- Протокол: **UDP**.

---

## Код
```python
# client.py

import socket

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9999
MESSAGE = 'Hello, server'
BUFFER_SIZE = 1024
TIMEOUT = 5.0  # сек

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT)

    try:
        print(f'Sending to {SERVER_HOST}:{SERVER_PORT}: {MESSAGE}')
        sock.sendto(MESSAGE.encode('utf-8'), (SERVER_HOST, SERVER_PORT))

        # ждём ответ от сервера
        data, server_addr = sock.recvfrom(BUFFER_SIZE)
        print(f'Received from server {server_addr}: {data.decode("utf-8")}')
    except socket.timeout:
        print('No response from server (timeout)')
    finally:
        sock.close()

if __name__ == '__main__':
    main()


# server.py
import socket

HOST = '127.0.0.1'   
PORT = 9999          

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    print(f'UDP server listening on {HOST}:{PORT} ...')

    try:
        while True:
            data, addr = sock.recvfrom(1024)  
            msg = data.decode('utf-8')
            print(f'Received from {addr}: {msg}')

            # Ответ клиенту
            if msg == 'Hello, server':
                reply = 'Hello, client'
            else:
                reply = 'Hello, client (reply)'

            sock.sendto(reply.encode('utf-8'), addr)
            print(f'Sent to {addr}: {reply}\n')
    except KeyboardInterrupt:
        print('\nServer stopped by user')
    finally:
        sock.close()

if __name__ == '__main__':
    main()


## Результат

![Результат работы клиента и сервера](/students/k3341/laboratory_works/Dzhavatov_Ilyas/laboratory_work_1/screenshots/task1.png)
