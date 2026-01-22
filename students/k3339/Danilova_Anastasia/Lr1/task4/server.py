import socket
import threading


class ChatServer:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.clients = []
        self.nicknames = []
        self.lock = threading.Lock()

    def sendAll(self, message, sender=None):
        """Отправляет сообщение в чат всем, кроме отправителя (но если флаг exclude_sender=False, то и ему тоже)"""
        with self.lock:
            for client in self.clients:
                if client == sender:
                    continue
                try:
                    client.send(message.encode('utf-8'))
                except:
                    self.remove_client(client)

    def remove_client(self, client):
        """Удаление клиента из списка"""
        if client in self.clients:
            index = self.clients.index(client)
            nickname = self.nicknames[index]

            with self.lock:
                self.clients.remove(client)
                self.nicknames.remove(nickname)

            leave_message = f"{nickname} left the chat"
            print(leave_message)
            self.sendAll(leave_message)
            client.close()

    def handle_client(self, client, address):
        """Обработка информации от клиента"""
        try:
            client.send("Input your nickname: ".encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8').strip()

            with self.lock:
                self.clients.append(client)
                self.nicknames.append(nickname)

            join_message = f"{nickname}'ve joined the chat!"
            print(join_message)
            self.sendAll(join_message)
            client.send("Welcome to the chat! To leave the chat type '/q'"
                        "\nTo change your username type '/n {new_name}'".encode('utf-8'))

            while True:
                message = client.recv(1024).decode('utf-8')

                if message == '/q':
                    break
                elif message.startswith('/n '):
                    if ' ' in message:
                        possible_nick = message.split(' ', 1)[1].strip()
                        if possible_nick:
                            new_nick = possible_nick
                            old_nick = nickname
                        else:
                            client.send("Nickname can't be void!".encode('utf-8'))
                            break
                    else:
                        client.send("Undefined input. Type /n {name} to change nickname".encode('utf-8'))
                        break

                    with self.lock:
                        index = self.clients.index(client)
                        self.nicknames[index] = new_nick
                    nickname = new_nick

                    nick_message_for_others = f"{old_nick} changed it's nickname to {new_nick}"
                    nick_message_for_self = f"You successfully changed it's nickname to {new_nick}"
                    self.sendAll(nick_message_for_others, sender=client)
                    client.send(nick_message_for_self.encode('utf-8'))
                elif message.strip():
                    formatted_message = f"{nickname}:{message}"
                    print(formatted_message)
                    self.sendAll(formatted_message, client)

        except Exception as e:
            print(f"Exception with client {address}: {e}")
        finally:
            self.remove_client(client)

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            sock.bind((self.host, self.port))
            sock.listen(5)
            print(f"Server runs at {self.host}:{self.port}")
            print(f"Chat is waiting for users to join")

            while True:
                client, address = sock.accept()
                print(f"User from {address} has joined")

                # запуск потока для обработки клиента
                client_thread = threading.Thread(target=self.handle_client, args=(client, address), daemon=True)
                client_thread.start()

        except KeyboardInterrupt:
            print(f"Shutting down the server...")
        except Exception as e:
            print(f"Exception: {e}")
        finally:
            sock.close()
            with self.lock:
                for client in self.clients:
                    client.close()


if __name__ == "__main__":
    server = ChatServer()
    server.start()
