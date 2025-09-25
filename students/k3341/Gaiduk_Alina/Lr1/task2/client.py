import socket

def run_client():
    a = input("Введите катет 1:")
    b = input("Введите катет 2:")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(('127.0.0.1', 11111))
        # Отправляем оба катета через пробел, кодируем
        client_socket.sendall(f"{a} {b}".encode("UTF-8"))
        server_message = client_socket.recv(1024).decode("UTF-8")
        print(f"Ответ сервера: {server_message}")

if __name__ == "__main__":
    run_client()