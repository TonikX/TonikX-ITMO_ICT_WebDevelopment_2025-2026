import socket
import threading

HOST = "127.0.0.1"
PORT = 50004

def handle_client(conn, addr):
    connections.append(conn)
    print("Connected by", addr)

    with conn:
        buffer = ""
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    continue

                buffer += data.decode("utf-8")
                while "\0" in buffer:
                    line, buffer = buffer.split("\0", 1)
                    for connect in connections:
                        if connect != conn:
                            connect.sendall((line + "\0").encode("utf-8"))
            except ConnectionResetError:
                break
    
    print("Connection closed", addr)
    connections.remove(conn)

connections = []

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
