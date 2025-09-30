import socket


HOST = "localhost"
PORT = 10001


def recv_until_prompt(sock):
    data = b""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
        if data.endswith(b"> "):
            break
    return data


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(s.recv(4096).decode("utf-8", errors="replace"), end="")
        while True:

            data = recv_until_prompt(s)
            if not data:
                break
            print(data.decode("utf-8", errors="replace"), end="")
            line = input()
            s.sendall((line + "\n").encode("utf-8"))
            if line.lower() in ("exit", "quit"):
                print(s.recv(4096).decode("utf-8", errors="replace"), end="")
                break

            data = recv_until_prompt(s)
            print(data.decode("utf-8", errors="replace"), end="")


if __name__ == "__main__":
    main()
