import socket
import math
import json

HOST = "127.0.0.1"
PORT = 8080
ENC = "utf-8"

# We decide on format of data incoming: "a b c\n"
# And to keep integrity of packages, delimeter all packages with "\n"
def recv_until(sock: socket.socket, delim: bytes = b"\n", bufsize: int = 1024) -> bytes:
    buf = bytearray()
    while True:
        # Receibe exactly N bytes
        chunk = sock.recv(bufsize)
        if not chunk:
            break
        buf += chunk
        # If "\n" in data, understand that it is last chunk
        if delim in chunk:
            break
    return bytes(buf)

def solve_quadratic(a: float, b: float, c: float) -> str:
    if a == 0.0:
        if b == 0.0:
            return "Unlimited number of solutions" if c == 0.0 else "No solution"
        x = -c / b
        return f"x = {x}"

    D = b*b - 4*a*c
    if D > 0:
        sqrtD = math.sqrt(D)
        x1 = (-b - sqrtD) / (2*a)
        x2 = (-b + sqrtD) / (2*a)
        x1, x2 = (x1, x2) if x1 <= x2 else (x2, x1)
        return f"x1 = {x1}, x2 = {x2} (D = {D})"
    elif D == 0:
        x = -b / (2*a)
        return f"x = {x} (D = 0)"
    else:
        sqrt_abs = math.sqrt(-D)
        re = -b / (2*a)
        im =  sqrt_abs / (2*a)
        return f"Complex solutions: {re} ± {im}i (D = {D})"

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        # srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind server on port
        srv.bind((HOST, PORT))
        # Set queue of clients to 1 - we can process only 1 at a time (right now without threading)
        srv.listen(1)
        print(f"TCP-server listening on {HOST}:{PORT}")
        try:
            while True:  # concurrently with 1 client

                # Accept connection from client
                conn, addr = srv.accept()
                with conn:
                    # Get all data
                    raw = recv_until(conn, b"\n")
                    print(f"Request from {addr}: {raw}")
                    if not raw:
                        continue
                    try:
                        # Get a,b,c from string
                        parts = raw.decode(ENC).strip().split()
                        a, b, c = map(float, parts[:3])
                        # Solve equation
                        result = solve_quadratic(a, b, c)
                        resp = ("OK: " + result + "\n").encode(ENC)
                    except Exception as e:
                        resp = (f"ERR: {e}\n").encode(ENC)

                    print(f"Response to {addr}: {resp}")

                    conn.sendall(resp)
        except KeyboardInterrupt:
            print("\nShutting down...")

if __name__ == "__main__":
    main()
