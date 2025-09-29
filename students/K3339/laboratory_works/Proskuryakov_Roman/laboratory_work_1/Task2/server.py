import socket
import math
import threading

HOST = "127.0.0.1"
PORT = 50002

def handle_request(line: str) -> str:
    parts = line.strip().split()
    if not parts:
        return "error: пустой запрос"

    op = parts[0].lower()
    try:
        if op == "hypotenuse" and len(parts) == 3:
            a = float(parts[1])
            b = float(parts[2])
            c = math.hypot(a, b)
            return f"ok {c}"
        elif op == "leg" and len(parts) == 3:
            c = float(parts[1])
            known = float(parts[2])
            if c <= known:
                return "error: гипотенуза должна быть больше катета"
            leg = math.sqrt(c*c - known*known)
            return f"ok {leg}"
        elif op == "quit":
            return "quit"
        else:
            return "error: неверный формат запроса"
    except ValueError:
        return "error: некорректные числа"

def handle_client(conn, addr):
    print("Connected by", addr)

    with conn:
        buffer = ""
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    continue

                buffer += data.decode("utf-8")
                print("Buffered data:", buffer)
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    response = handle_request(line)
                    if response == "quit":
                        conn.sendall(b"ok closing\n")
                        print("Client requested quit", addr)
                        print("Connection closed", addr)
                        return
                    
                    conn.sendall((response + "\n").encode("utf-8"))
            except ConnectionResetError:
                break
    
    print("Connection closed", addr)

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client,  args=[conn, addr])
            thread.start()

if __name__ == "__main__":
    run_server()
