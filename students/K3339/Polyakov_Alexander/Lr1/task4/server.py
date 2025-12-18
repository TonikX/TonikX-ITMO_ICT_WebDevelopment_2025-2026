import socket
import threading
import json

class ClientQuit(Exception):
    pass

HOST = "127.0.0.1"
PORT = 7000
ENC = "utf-8"

clients = {}
# Mutex to protect concurrent access to `clients`
clients_lock = threading.Lock()

def send_json(conn: socket.socket, obj: dict):
    """Send one JSON object as a single NDJSON line."""
    try:
        data = (json.dumps(obj, ensure_ascii=False) + "\n").encode(ENC)
        conn.sendall(data)  # blocking send; ensures the whole buffer goes out
    except OSError:
        pass

def broadcast_json(obj: dict, exclude: socket.socket | None = None):
    # Take a snapshot under lock to avoid iterating while the dict is modified
    with clients_lock:
        conns = list(clients.keys())
    for c in conns:
        if c is exclude:
            continue
        send_json(c, obj)

def remove_client(conn: socket.socket):
    with clients_lock:
        info = clients.pop(conn, None)
    try:
        conn.close()
    except OSError:
        pass
    return info

def handle_client(conn: socket.socket, addr):
    buf = bytearray()

    def recv_chunk() -> bool:
        try:
            chunk = conn.recv(4096)
            if not chunk:
                return False  # peer closed
            buf.extend(chunk)
            return True
        except OSError:
            return False

    # process hello message
    name = None
    while b"\n" not in buf:
        if not recv_chunk():
            remove_client(conn)
            return
    line, _, rest = buf.partition(b"\n")
    buf = bytearray(rest)
    try:
        hello = json.loads(line.decode(ENC).strip())
        # Validate structure of the hello message
        if not (isinstance(hello, dict) and hello.get("type") == "hello" and isinstance(hello.get("name"), str)):
            raise ValueError("bad hello object")
        name = hello["name"].strip() or f"user@{addr[1]}"
    except Exception:
        name = f"user@{addr[1]}"

    # Register the client (protected by lock)
    with clients_lock:
        clients[conn] = {"name": name, "addr": addr}

    # Send system message + broadcast it to other connections
    send_json(conn, {"name": "system", "message": f"Welcome, {name}! Type /quit to leave"})
    broadcast_json({"name": "system", "message": f"{name} joined"}, exclude=conn)

    # process regular messages
    try:
        while True:
            # Drain all complete lines currently in buffer
            while b"\n" in buf:
                line, _, buf = buf.partition(b"\n")
                text = line.decode(ENC).strip()
                if not text:
                    continue

                try:
                    obj = json.loads(text)
                except json.JSONDecodeError:
                    continue

                # Handle logout command (as message content)
                if isinstance(obj, dict) and obj.get("message") == "/quit":
                    raise ClientQuit

                # Enforce sender's name on the server (avoid spoofing)
                out = {
                    "name": name,
                    "message": (obj.get("message") if isinstance(obj, dict) else str(obj))
                }
                if out["message"]:
                    broadcast_json(out, exclude=conn)

            if not recv_chunk():
                break
    finally:
        info = remove_client(conn)
        if info:
            broadcast_json({"name": "system", "message": f"{info['name']} left"})

def main():
    # Create socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        # Rebind quickly after restart
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind socker to listen on set port
        srv.bind((HOST, PORT))
        srv.listen(50) # set length of queue
        print(f"Chat server is listening  on {HOST}:{PORT}")
        try:
            while True:
                conn, addr = srv.accept()
                # Reduce interactive latency for small writes
                conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                # Start a thread for each client
                threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
        except KeyboardInterrupt:
            print("\nStopping server...")
        finally:
            with clients_lock:
                conns = list(clients.keys())
            for c in conns:
                try: c.shutdown(socket.SHUT_RDWR)
                except OSError: pass
                try: c.close()
                except OSError: pass

if __name__ == "__main__":
    main()
