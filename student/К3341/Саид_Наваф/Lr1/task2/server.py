import socket
from mathematics import parse_math

HOST = "127.0.0.1"
PORT = 8082

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"TCP calculator server listening on {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        with conn:
            print("Connected by", addr)
            data = conn.recv(4096)
            if not data:
                continue
            try:
                math = parse_math(data.decode())
                result = math.do_math()
                conn.sendall(str(result).encode())
            except Exception as e:
                conn.sendall(f"ERROR: {e}".encode())