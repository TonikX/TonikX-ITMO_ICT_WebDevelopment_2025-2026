import socket
import threading


class ChatClient:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = True

    def receive_message(self):
        while self.running:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print(f"\n{message}\n", end='')
            except:
                break
        print(f"\n Connection with server was lost")
        self.running = False

    def send_message(self):
        while self.running:
            try:
                message = input("You: ")
                if not self.running:
                    break

                if message.lower() == '/q':
                    self.socket.send(message.encode('utf-8'))
                    break
                elif message.strip():
                    self.socket.send(message.encode('utf-8'))

            except KeyboardInterrupt:
                self.socket.send('q'.encode('utf-8'))
                break
            except Exception as e:
                print(f"Exception: {e}")
                break

    def start(self):
        try:
            self.socket.connect((self.host, self.port))
            print("You've successfully joined to the chat!")

            # daemon=True — это поток, который не препятствует завершению процесса
            receive_thread = threading.Thread(target=self.receive_message, daemon=True)
            receive_thread.start()

            self.send_message()

        except ConnectionRefusedError:
            print("Failed to join the server")
        except Exception as e:
            print(f"Exception {e}")
        finally:
            self.running = False
            self.socket.close()
            print("Client is shutting down")


if __name__ == '__main__':
    client = ChatClient()
    client.start()
