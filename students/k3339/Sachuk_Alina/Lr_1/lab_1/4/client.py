import socket
import threading


class MessageReceiverThread(threading.Thread):
    def __init__(self, connection_sock: socket.socket):
        super().__init__()
        self.connection_sock = connection_sock
        self.is_server_closed = False

    def run(self) -> None:
        while not terminate_threads and not self.is_server_closed:
            try:
                data = self.connection_sock.recv(1024)
                if not data:
                    print(
                        "Соединение закрыто сервером. "
                    )
                    self.is_server_closed = True
                    break
                print(data.decode())
            except socket.timeout:
                continue


client_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_conn.connect(("127.0.0.1", 8080))
client_conn.settimeout(1)

terminate_threads = False
receiver_thread = MessageReceiverThread(client_conn)
receiver_thread.start()

try:
    while True:
        if receiver_thread.is_server_closed:
            break
        try:
            user_input = input()
            client_conn.sendall(user_input.encode())
        except KeyboardInterrupt:
            print("Вы покинули чат.")
            break
except KeyboardInterrupt:
    print("Вы покинули чат.")
finally:
    terminate_threads = True
    receiver_thread.join()
    client_conn.close()