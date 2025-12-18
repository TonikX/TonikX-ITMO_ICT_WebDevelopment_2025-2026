import socket
import threading
import json

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 7000
ENC = "utf-8"

def send_json(sock: socket.socket, obj: dict):
    sock.sendall((json.dumps(obj, ensure_ascii=False) + "\n").encode(ENC))

def recv_loop(sock: socket.socket):
    buf = bytearray()
    try:
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                print("\n* Соединение закрыто сервером")
                break
            buf.extend(chunk)
            while b"\n" in buf:
                line, _, buf = buf.partition(b"\n")
                try:
                    obj = json.loads(line.decode(ENC).strip())
                    if isinstance(obj, dict) and "name" in obj and "message" in obj:
                        print(f"[{obj['name']}] {obj['message']}")
                    else:
                        print(line.decode(ENC, errors="replace").strip())
                except json.JSONDecodeError:
                    print(line.decode(ENC, errors="replace").strip())
    except OSError:
        pass

def main():
    nick = input("You username: ").strip() or "anon"
    with socket.create_connection((SERVER_HOST, SERVER_PORT)) as sock:
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        # Send hello message to register in system
        send_json(sock, {"type": "hello", "name": nick})

        # Start process of receiving messages in thread
        t = threading.Thread(target=recv_loop, args=(sock,), daemon=True)
        t.start()

        # Start loop of sending messages
        try:
            while True:
                try:
                    text = input()
                except EOFError:
                    text = "/quit"
                if not text:
                    continue

                # /quit message
                if text == "/quit":
                    try: send_json(sock, {"name": nick, "message": "/quit"})
                    except OSError: pass
                    break

                # regular message
                try:
                    send_json(sock, {"name": nick, "message": text})
                except OSError:
                    print("* Connection lost")
                    break
        except KeyboardInterrupt:
            try: send_json(sock, {"name": nick, "message": "/quit"})
            except OSError: pass
        finally:
            try:
                sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass

if __name__ == "__main__":
    main()
