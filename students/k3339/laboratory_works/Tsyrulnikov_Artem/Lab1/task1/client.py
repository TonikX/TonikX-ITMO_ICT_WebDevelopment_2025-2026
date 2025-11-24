import socket


class Config:
    HOST = "localhost"
    PORT = 8001


def run_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (Config.HOST, Config.PORT)

    message = "Hello, server"
    print(f"-> {message}")
    client_socket.sendto(message.encode("utf-8"), server_address)

    data, _ = client_socket.recvfrom(1024)
    response = data.decode("utf-8")
    print(f"<- {response}")

    client_socket.close()


if __name__ == "__main__":
    run_client()
