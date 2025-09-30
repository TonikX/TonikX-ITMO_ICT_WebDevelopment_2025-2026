import socket
import threading

HOST = "0.0.0.0"
PORT = 12345

clients = {}
clients_lock = threading.Lock()

def broadcast(message, exclude_sock=None):
    """Отправить message всем клиентам, кроме exclude_sock (если задан)."""
    with clients_lock:
        for sock in list(clients.keys()):
            if sock is exclude_sock:
                continue
            try:
                sock.sendall(message.encode('utf-8'))
            except Exception:
                # если не получилось отправить — закрываем сокет
                try:
                    sock.close()
                except:
                    pass
                del clients[sock]

def handle_client(conn, addr):
    """Обработка одного клиента в отдельном потоке."""
    try:
        conn.sendall("Введите ваше имя: ".encode('utf-8'))
        name_bytes = conn.recv(1024)
        if not name_bytes:
            conn.close()
            return
        username = name_bytes.decode('utf-8').strip() or f"{addr}"
        with clients_lock:
            clients[conn] = username

        broadcast(f"*** {username} присоединился(ась) к чату ***\n")

        while True:
            data = conn.recv(4096)
            if not data:
                break
            text = data.decode('utf-8').strip()
            if text.lower() in ('/quit', '/exit'):
                break
            # Формируем сообщение с ником
            msg = f"[{username}] {text}\n"
            print(msg, end='')  # лог на сервере
            broadcast(msg, exclude_sock=conn)
    except Exception as e:
        print("Ошибка в обработке клиента:", e)
    finally:
        # Удаляем клиента и оповещаем остальных
        with clients_lock:
            if conn in clients:
                left_name = clients.pop(conn)
            else:
                left_name = str(addr)
        try:
            conn.close()
        except:
            pass
        broadcast(f"*** {left_name} покинул(а) чат ***\n")

def main():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen(100)
    print(f"TCP чат-сервер запущен на {HOST}:{PORT}")

    try:
        while True:
            conn, addr = srv.accept()
            print("Подключился:", addr)
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("Сервер останавливается...")
    finally:
        srv.close()
        with clients_lock:
            for s in list(clients.keys()):
                try:
                    s.close()
                except:
                    pass
        print("Сервер остановлен.")

if __name__ == "__main__":
    main()
