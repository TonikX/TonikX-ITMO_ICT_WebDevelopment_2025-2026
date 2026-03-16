import socket
import threading

class ChatClient:
    def __init__(self, host='localhost', port=8911):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = False
    def start(self):
        try:
            self.socket.connect((self.host, self.port))
            self.running = True
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            print("Connected. To end send: /exit")
            while self.running:
                message = input()
                if message == '/exit':
                    break
                self.socket.send(message.encode())
        except Exception as e:
            print(f"Connection error: {e}")
        finally:
            self.stop()

    def receive_messages(self):
        while self.running:
            try:
                message = self.socket.recv(1024).decode()
                if not message:
                    break
                print(message)
            except:
                break

    def stop(self):
        self.running = False
        self.socket.close()
        print("Disconnected")

if __name__ == "__main__":
    client = ChatClient()
    client.start()
