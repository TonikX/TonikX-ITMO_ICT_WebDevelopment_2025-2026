import json
import socket


class Config:
    HOST = "0.0.0.0"
    PORT = 8002
    BUFFER_SIZE = 1024


def calculate_trapezoid_area(a, b, h):
    return (a + b) * h / 2


def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((Config.HOST, Config.PORT))
    server_socket.listen(5)
    print(f"Сервер запущен на {Config.HOST}:{Config.PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Подключение от {client_address[0]}:{client_address[1]}")

        try:
            data = client_socket.recv(Config.BUFFER_SIZE)
            message = data.decode("utf-8")
            print(f"{client_address[0]}:{client_address[1]} -> {message}")

            params = json.loads(message)
            a = float(params["a"])
            b = float(params["b"])
            h = float(params["h"])

            area = calculate_trapezoid_area(a, b, h)
            response = json.dumps({"result": area})

            client_socket.send(response.encode("utf-8"))

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            response = json.dumps({"error": f"Ошибка в данных: {str(e)}"})
            client_socket.send(response.encode("utf-8"))

        finally:
            print(f"{client_address[0]}:{client_address[1]} <- {response}")
            client_socket.close()


if __name__ == "__main__":
    run_server()
