import socket
import os

HOST = '127.0.0.1'   # localhost
PORT = 8080          # порт сервера
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_server():
    # создаем сокет
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Сервер запущен на http://{HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Подключился клиент: {addr}")

                # request = conn.recv(1024).decode('utf-8')
                # print("Запрос клиента:\n", request)

                try:
                    index_path = os.path.join(BASE_DIR, "index.html")

                    with open(index_path, "r", encoding="utf-8") as f:
                        html_content = f.read()
                except FileNotFoundError:
                    html_content = "<h1>Файл index.html не найден</h1>"

                # формируем HTTP-ответ
                response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/html; charset=utf-8\r\n"
                    f"Content-Length: {len(html_content.encode('utf-8'))}\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                    f"{html_content}"
                )

                conn.sendall(response.encode('utf-8'))

if __name__ == "__main__":
    run_server()
