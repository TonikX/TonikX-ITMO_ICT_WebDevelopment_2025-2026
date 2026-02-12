import socket


def run_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8080))
    client_socket.sendall(input('Введите через пробел основание и высоту' \
    'для расчета площади параллелограмма: ').encode())

    response = client_socket.recv(1024)
    print(f'Ответ: {response.decode()}')

    client_socket.close()

if __name__ == "__main__":
    run_client()