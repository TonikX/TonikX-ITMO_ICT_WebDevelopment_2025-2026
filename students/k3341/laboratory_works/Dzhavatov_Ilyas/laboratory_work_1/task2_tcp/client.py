# client.py
import socket

HOST = '127.0.0.1'
PORT = 5000

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    # Ввод данных с клавиатуры
    base = input("Введите основание параллелограмма: ")
    height = input("Введите высоту параллелограмма: ")

    # Отправляем данные на сервер
    message = f"{base} {height}"
    sock.sendall(message.encode('utf-8'))
    print(f"Sent to server: {message}")

    # Ждём ответ
    data = sock.recv(1024).decode('utf-8')
    print(f"Received from server: {data}")

    sock.close()

if __name__ == '__main__':
    main()
