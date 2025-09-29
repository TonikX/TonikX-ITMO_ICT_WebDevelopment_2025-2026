import socket
import json

HOST = "localhost"
PORT = 14905
CODING = "utf-8"


def send_post_req(discipline: str, mark: str):
    body = json.dumps({"discipline": discipline, "mark": mark})
    body_bytes = body.encode(CODING)

    request = (
        f"POST / HTTP/1.1\r\n"
        f"Host: {HOST}:{PORT}\r\n"
        f"Content-Type: application/json\r\n"
        f"Content-Length: {len(body_bytes)}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    ).encode(CODING) + body_bytes

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(request)

        response = sock.recv(4096)

    return response.decode(CODING, errors="replace")


if __name__ == "__main__":
    try:
        while True:
            discipline = input("\nEnter the name of the discipline: ").strip().lower()
            while True:
                try:
                    mark = float(input("Enter the score: ").strip())
                    if not 0 <= mark <= 100:
                        print(
                            "\033[91mInput must be greater than zero and smaller than 100!\033[0m"
                        )
                        continue
                    break
                except ValueError:
                    print("\033[91mPlease enter a valid number!\033[0m")

            resp = send_post_req(discipline, mark)
            print("\nServer response:")
            print(resp.split("\r\n\r\n", 1))

    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye!")
