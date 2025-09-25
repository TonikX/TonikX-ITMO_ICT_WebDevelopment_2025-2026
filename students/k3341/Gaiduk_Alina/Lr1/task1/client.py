import socket

def run_client():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_message = "Hello, server"
        client_socket.sendto(client_message.encode("UTF-8"), ('127.0.0.1', 11111))
        # ждем ответную датаграмму
        server_message, _ = client_socket.recvfrom(1024)
        print(server_message.decode("UTF-8"))

if __name__ == "__main__":
    run_client()

