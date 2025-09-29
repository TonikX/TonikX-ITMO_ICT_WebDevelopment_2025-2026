import socket

HOST = "127.0.0.1"
PORT = 9999

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    print(f"[UDP SERVER] Listening on {HOST}:{PORT}")
    while True:
        data, addr = sock.recvfrom(1024)
        msg = data.decode("utf-8", errors="replace")
        print(f"[RECV from {addr}] {msg}")
        if msg.strip().lower() == "hello, server":
            sock.sendto(b"Hello, client", addr)
        else:
            sock.sendto(b"Unknown message", addr)

if __name__ == "__main__":
    main()
