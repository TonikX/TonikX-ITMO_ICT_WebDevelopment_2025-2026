import socket
import threading
import json

HOST = "127.0.0.1"
PORT = 8082

def recv_loop(s):
    while True:
        data = s.recv(4096)
        if not data:
            break
        try:
            msg = json.loads(data.decode())
            print(f"[{msg['id']}] {msg['msg']}")
        except Exception:
            print("Received:", data.decode())

def send_loop(s):
    while True:
        try:
            text = input()
            if not text:
                continue
            s.sendall(text.encode())
        except EOFError:
            break

def main():
    user_id = input("Enter your id: ").strip()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(user_id.encode())

    threading.Thread(target=recv_loop, args=(s,), daemon=True).start()
    send_loop(s)
    s.close()

if __name__ == "__main__":
    main()