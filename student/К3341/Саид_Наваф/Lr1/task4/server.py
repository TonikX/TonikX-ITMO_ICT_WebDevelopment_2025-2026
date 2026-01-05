import socket
import threading
import json


HOST = "127.0.0.1"
PORT = 8082

clients = {}  # id -> conn
clients_lock = threading.Lock()

def handle_client(conn, addr):
    try:
        # First message should be client id (simple protocol)
        client_id = conn.recv(1024).decode().strip()
        if not client_id:
            conn.close()
            return

        with clients_lock:
            if client_id in clients:
                conn.sendall(b"ID_USED")
                conn.close()
                return
            clients[client_id] = conn
        print("Client connected:", client_id, addr)
        while True:
            data = conn.recv(4096)
            if not data:
                break
            text = data.decode().strip()
            print(f"Received from {client_id}: {text}")
            msg_obj = {"id": client_id, "msg": text}
            broadcast(json.dumps(msg_obj))
    finally:
        with clients_lock:
            # remove
            for k, v in list(clients.items()):
                if v is conn:
                    del clients[k]
                    break
        conn.close()
        print("Client disconnected:", client_id)

def broadcast(message: str):
    with clients_lock:
        for cid, cconn in list(clients.items()):
            try:
                cconn.sendall(message.encode())
            except Exception:
                # ignore send errors, remove later in recv loop
                pass

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Chat server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()