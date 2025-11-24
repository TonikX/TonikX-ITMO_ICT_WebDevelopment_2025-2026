import json
import socket


class Config:
    HOST = "localhost"
    PORT = 8002


def get_input_safe(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Введите корректное число!")


def get_trapezoid_params():
    print("Введите параметры трапеции:")
    a = get_input_safe("Основание a: ")
    b = get_input_safe("Основание b: ")
    h = get_input_safe("Высота h: ")
    return a, b, h


def run_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((Config.HOST, Config.PORT))
    print(f"Подключение к серверу {Config.HOST}:{Config.PORT}")

    a, b, h = get_trapezoid_params()

    message = json.dumps({"a": a, "b": b, "h": h})
    print(f"-> {message}")

    client_socket.send(message.encode("utf-8"))

    data = client_socket.recv(1024)
    response = data.decode("utf-8")
    print(f"<- {response}")

    result = json.loads(response)
    if "result" in result:
        print(f"Площадь трапеции: {result['result']}")
    elif "error" in result:
        print(f"Ошибка: {result['error']}")

    client_socket.close()


if __name__ == "__main__":
    run_client()
