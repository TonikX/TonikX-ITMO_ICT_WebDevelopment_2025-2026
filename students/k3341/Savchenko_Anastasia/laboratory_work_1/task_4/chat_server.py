import socket
import threading

clients = [] # глобальный список всех подключённых клиентских сокетов
lock = threading.Lock() # объект для синхронизации потоков

#  Функция широковещательной рассылки
def send_to_all(msg, sender=None):
    with lock:
        for client in clients:
            if client != sender:
                try:
                    client.send(msg.encode())
                except:
                    clients.remove(client)

# Функция-обработчик клиента (работает в отдельном потоке)
def handle_client(client, addr):
    try:
        nickname = client.recv(1024).decode().strip()
        if not nickname:
            nickname = f"user_{addr[1]}"

        with lock:
            clients.append(client)

        send_to_all(f"{nickname} присоединился")

        while True:
            msg = client.recv(1024).decode().strip()
            if not msg or msg == "/quit":
                break
            send_to_all(f"{nickname}: {msg}", sender=client)
    except:
        pass
    finally:
        with lock:
            if client in clients:
                clients.remove(client)
        try:
            client.close()
        except:
            pass


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 1238))
server.listen()

print("Сервер запущен на порту 1238")

while True:
    client, addr = server.accept()
    threading.Thread(target=handle_client, args=(client, addr), daemon=True).start()