import socket
import threading

HOST = "0.0.0.0"
PORT = 9091

clients = set()
clients_lock = threading.Lock()

def broadcast(msg: str, exclude=None):
    # функция рассылки сообщений всем клиентам
    with clients_lock:
        dead = []
        for sock in clients:
            # самому себе не надо отправлять 
            if sock is exclude:
                continue
            try:
                sock.sendall((msg + "\n").encode("utf-8"))
            except Exception:
                dead.append(sock)
        for d in dead:
            # удаляем мертвые соеденения 
            clients.discard(d)
            try:
                d.close()
            except Exception:
                pass

def handle_client(conn: socket.socket, addr):
    # оборачиваем сокет "файлом", чтобы удобно читать по строкам
    f = conn.makefile("r", encoding="utf-8", newline="\n")
    try:
        conn.sendall("Введите никнейм: ".encode("utf-8"))
        nickname = f.readline()
        if not nickname:
            return
        nickname = nickname.strip()
        if not nickname:
            nickname = f"{addr[0]}:{addr[1]}"

        join_msg = f"{nickname} присоединился к чату"
        print(join_msg)
        broadcast(join_msg, exclude=None)

        # добавляем клиента в список клиентов
        with clients_lock:
            clients.add(conn)

        # основной цикл чтения сообщений построчно
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            if line == "/quit":
                break
            broadcast(f"[{nickname}] {line}", exclude=conn)

    except Exception as e:
        # можно логировать e, но для учебной оставим тихо
        pass
    finally:
        with clients_lock:
            if conn in clients:
                clients.remove(conn)
        try:
            conn.close()
        except Exception:
            pass
        leave_msg = f"{nickname} вышел из чата"
        print(leave_msg)
        broadcast(leave_msg, exclude=None)

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # быстрый перезапуск порта
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(100)
    print(f"Сервер чата запущен на {HOST}:{PORT}")

    try:
        # цикл приема клиентов 
        while True:
            conn, addr = server.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()
    except KeyboardInterrupt:
        # KeyboardInterrupt выбрасывает сочетание ctr c 
        print("\nОстановка сервера...")
    finally:
        with clients_lock:
            for c in list(clients):
                try:
                    c.close()
                except Exception:
                    pass
            clients.clear()
        server.close()

if __name__ == "__main__":
    main()
