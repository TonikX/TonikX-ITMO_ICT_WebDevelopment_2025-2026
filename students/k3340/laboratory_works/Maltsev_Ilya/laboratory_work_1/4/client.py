import socket
import threading


class MessageReceiverThread(threading.Thread):
    def __init__(self, connection_sock: socket.socket, stop_event: threading.Event):
        super().__init__()
        self.connection_sock = connection_sock
        self.stop_event = stop_event

    def run(self) -> None:
        while not self.stop_event.is_set():
            try:
                data = self.connection_sock.recv(1024)
                if not data:
                    print("Соединение закрыто сервером.")
                    self.stop_event.set()
                    break
                print(data.decode())
            except socket.timeout:
                continue
            except OSError:
                break


client_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_conn.connect(("127.0.0.1", 8080))
client_conn.settimeout(1)

stop_event = threading.Event()
receiver_thread = MessageReceiverThread(client_conn, stop_event)
receiver_thread.start()

try:
    while not stop_event.is_set():
        try:
            user_input = input()
            client_conn.sendall(user_input.encode())
        except KeyboardInterrupt:
            print("Вы покинули чат.")
            break
        except BrokenPipeError:
            print("Соединение разорвано.")
            stop_event.set()
            break
except KeyboardInterrupt:
    print("Вы покинули чат.")
finally:
    stop_event.set()
    receiver_thread.join()
    client_conn.close()
