import socket
import threading
from config import HOST, PORT
from msg_dataclass import Message

clients = []

def send_message(client_socket: socket.socket, msg: Message):
    global clients
    msg = str(msg).encode()
    for client in clients:
        if client != client_socket:
            try:
                client.send(msg)
            except Exception as e:
                print(f"Error {e} while sending message to client, stoping it's connection")
                try:
                    client.close()
                except:
                    pass


def process_client(client_socket: socket.socket, addr: tuple):
    global clients

    try:
        print(f"New user with addr: {addr}")
        while True:
            msg = client_socket.recv(16384).decode()
            msg = Message.parse_msg(msg)
            if msg.type == "quit":
                break
            msg.author = addr[1]
            send_message(client_socket, msg)
    except Exception as e:
        print(f"error {e} while processing client {addr}")
    finally:
        print(f"stoping connection and thread for client {addr}")
        try:
            msg = Message(type="stop", author="server")
            client_socket.send(str(msg).encode())
            client_socket.close()
        except:
            pass
        clients.remove(client_socket)


conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.bind((HOST, PORT))
conn.listen(10)
try:
    while True:
        client_socket, addr = conn.accept()
        clients.append(client_socket)
        new_client_thread = threading.Thread(target=process_client, args=(client_socket, addr), daemon=True)
        new_client_thread.start()
except Exception as e:
    print(f"Error {e} while server running, trying to send messages of stop, and shutting down")
    try:
        msg = Message(type="stop", author="server")
        send_message(conn, msg)
    except:
        print("err")
finally: 
    conn.close()
