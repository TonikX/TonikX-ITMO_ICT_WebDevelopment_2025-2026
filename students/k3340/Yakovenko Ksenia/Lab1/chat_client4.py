import socket
import threading

HOST = "127.0.0.1"
PORT = 30114

def receive(sock):
    while True:
        try:
            msg = sock.recv(1996).decode()
            if msg:
                print("\n", msg)
        except:
            break

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

local_port = sock.getsockname()[1]

# stream for getting messages
thread = threading.Thread(target=receive, args=(sock,))
thread.start()

print("Connected to the chat! Enter your message:")

while True:
    msg = f"{input()}"
    sock.sendall(msg.encode())
