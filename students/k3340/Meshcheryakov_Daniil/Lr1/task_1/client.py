import socket
import sys

HOST = "127.0.0.1"
PORT = 9999
MESSAGE = "Hello, server"

def main():
    message = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else MESSAGE
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(3)
    sock.sendto(message.encode("utf-8"), (HOST, PORT))
    try:
        data, _ = sock.recvfrom(1024)
        print("[REPLY]", data.decode("utf-8", errors="replace"))
    except socket.timeout:
        print("No response (timeout).")

if __name__ == "__main__":
    main()
