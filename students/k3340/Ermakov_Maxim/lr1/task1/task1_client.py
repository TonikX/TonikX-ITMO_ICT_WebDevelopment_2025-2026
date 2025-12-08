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
