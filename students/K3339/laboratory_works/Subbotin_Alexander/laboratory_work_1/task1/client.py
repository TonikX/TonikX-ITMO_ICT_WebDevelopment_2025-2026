import socket

HOST = 'localhost'
PORT = 8080

def udp_client():
    conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    conn.connect((HOST, PORT))
    conn.send(b"Hello, server \n")

    resp = conn.recv(1024)
    res = resp.decode("utf-8")
    print(f'\nответ от сервера: {res}')

    conn.close()

if __name__ == "__main__":
    udp_client()
