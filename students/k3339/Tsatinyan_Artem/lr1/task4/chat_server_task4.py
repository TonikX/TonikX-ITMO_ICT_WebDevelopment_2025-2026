import socket
import threading

HOST = "127.0.0.1"
PORT = 7070
ENC = "utf-8"
BUF = 4096

# Словарь подключённых клиентов: conn -> nickname
clients = {}
# Блокировка для потокобезопасного доступа к clients
clients_lock = threading.Lock()

# Рассылает сообщение всем клиентам.
def broadcast(message: str, exclude_conn=None):
    data = (message + "\n").encode(ENC)
    with clients_lock:
        for conn in list(clients.keys()):
            if conn is exclude_conn:
                continue
            try:
                conn.sendall(data)
            except OSError:
                # Если соединение сломано — закрываем и удаляем из списка
                try:
                    conn.close()
                except OSError:
                    pass
                clients.pop(conn, None)

def handle_client(conn: socket.socket, addr):
    """
    Обрабатывает отдельного клиента:
    - принимает его никнейм
    - слушает команды/сообщения
    - обрабатывает отключение
    """
    nickname = None
    try:
        # Первое сообщение от клиента должно быть его никнейм
        raw = conn.recv(BUF)
        if not raw:
            return
        first = raw.decode(ENC, errors="replace").strip()
        if not first.startswith("NICK:"):
            conn.sendall("ERR: send 'NICK:<имя>' сначала\n".encode(ENC))
            return
        # Если ник пустой, назначаем user_<порт>
        nickname = first.split(":", 1)[1].strip() or f"user_{addr[1]}"

        # Добавляем клиента в общий список
        with clients_lock:
            clients[conn] = nickname

        # Подтверждаем вход
        conn.sendall(f"OK: привет, {nickname}! Команды: /list, /quit\n".encode(ENC))
        broadcast(f"* {nickname} присоединился к чату", exclude_conn=conn)

        while True:
            data = conn.recv(BUF)
            if not data:
                break
            text = data.decode(ENC, errors="replace").rstrip("\r\n")

            if text == "/quit":
                conn.sendall("OK: выходим...\n".encode(ENC))
                break
            if text == "/list":
                with clients_lock:
                    names = ", ".join(sorted(clients.values()))
                conn.sendall(f"Участники: {names}\n".encode(ENC))
                continue

            broadcast(f"[{nickname}] {text}", exclude_conn=None)

    except ConnectionResetError:
        # Клиент внезапно отключился
        pass
    finally:
        # Убираем клиента из списка при выходе
        left_name = None
        with clients_lock:
            left_name = clients.pop(conn, None)
        if left_name:
            broadcast(f"* {left_name} покинул чат")
        try:
            conn.close()
        except OSError:
            pass

def main():
    print(f"Чат-сервер TCP слушает на {HOST}:{PORT}. Остановить: Ctrl+C")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORT))
        srv.listen(50)
        while True:
            conn, addr = srv.accept()
            # Для каждого клиента создаём отдельный поток
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()

if __name__ == "__main__":
    main()
