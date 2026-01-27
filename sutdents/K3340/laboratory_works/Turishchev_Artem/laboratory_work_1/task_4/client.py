import socket
import threading
from config import HOST, PORT
from msg_dataclass import Message


def reciever(conn: socket.socket, stop: threading.Event):
    while not stop.is_set():
        try:
            msg = conn.recv(16384).decode()
            msg = Message.parse_msg(msg)
            if msg.type == "stop" and msg.author == "server":
                stop.set()
                print(f"recieved stop message from server")
                break
            else:
                print(f"{msg.author}: {msg.msg}")
        except Exception as e:
            print(f"error {e} while recieving")
            stop.set()

def sender(conn: socket.socket, stop: threading.Event):
    try:
        while not stop.is_set():
            msg = input()
            if msg == "exit":
                stop.set()
                print("Exit command recieved")
                break
            msg = Message(msg=msg)
            conn.send(str(msg).encode())
    except Exception as e:
        print(f"error {e} during sending msg")
        stop.set()

print('Type messages to send, type "exit" to stop client')
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((HOST, PORT))
stop = threading.Event()
reciever_thread = threading.Thread(target=reciever, args=(conn, stop), daemon=True)
sender_thread = threading.Thread(target=sender, args=(conn, stop), daemon=True)

reciever_thread.start()
sender_thread.start()
try:
    while not stop.is_set():
        stop.wait(timeout=0.5)
except Exception as e:
    print(f"Error {e} in client")
finally:
    try:
        msg = Message(type="quit")
        conn.send(str(msg).encode())
    except:
        pass
    print("shutting down client")
    try:
        conn.close()
    except:
        pass