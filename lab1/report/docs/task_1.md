### Задание 1 (UDP)

Сервер:

```bash
import socket


HOST = "localhost"
PORT = 8080


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ("localhost", 8080)

    try:
        message = "Hello, server"
        print(f"Sending...")
        sock.sendto(message.encode(), server_address)
        data, _ = sock.recvfrom(1024)
        print(f"Response: {data.decode()}")
    finally:
        sock.close()


if __name__ == "__main__":
    main()
```

```bash
python task1_udp/server_udp.py
```
Клиент:
```bash
import socket


HOST = "localhost"
PORT = 8080


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    print(f"Server is working")

    try:
        while True:
            data, client_address = sock.recvfrom(1024)
            print(f"Response: {data.decode()}")
            reply = "Hello, client"
            sock.sendto(reply.encode(), client_address)
            print(f"Request is sended")
    except KeyboardInterrupt:
        print('\nShutting down the server')
    finally:
        sock.close()


if __name__ == "__main__":
    main()
```


```bash
python task1_udp/client_udp.py
```