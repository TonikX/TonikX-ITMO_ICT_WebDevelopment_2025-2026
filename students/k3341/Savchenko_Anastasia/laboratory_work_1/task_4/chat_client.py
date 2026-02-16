import socket
import threading

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(4096).decode()
            if not msg:
                break
            print(f"\n{msg}\n> ", end="")
        except:
            break

nickname = input("Введите ник: ").strip()
if not nickname:
    nickname = "user"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 1238))

sock.send(f"{nickname}\n".encode())

threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

print("> ", end="")

while True:
    msg = input()
    if msg.strip().lower() == "/quit":
        sock.send(b"/quit\n")
        break
    sock.send(f"{msg}\n".encode())
    print("> ", end="")

sock.close()