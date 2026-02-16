import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9999))
name = input("Enter your name: ")
client.send(name.encode())

def receive():
    while True:
        try:
            msg = client.recv(1024).decode()
            if not msg:
                break
            print(msg)
        except:
            break
    client.close()

threading.Thread(target=receive, daemon=True).start()
while True:
    msg = input()
    if not msg:
        break
    client.send(msg.encode())
client.close()
