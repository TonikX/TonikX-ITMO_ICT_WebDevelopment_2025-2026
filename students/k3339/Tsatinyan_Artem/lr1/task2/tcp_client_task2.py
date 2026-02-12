import socket
import json

HOST = "127.0.0.1"
PORT = 9090
ENC = "utf-8"
BUF = 4096
TIMEOUT = 5.0

def prompt_float(name: str) -> float:
    while True:
        try:
            value = float(input(f"Введите {name}: ").strip().replace(",", "."))
            return value
        except ValueError:
            print("Нужно число. Попробуйте ещё раз.")

def main():
    print("Задание 2 (вариант 3): площадь трапеции S = (a + b) / 2 * h")
    a = prompt_float("основание a")
    b = prompt_float("основание b")
    h = prompt_float("высоту h")

    req = {"op": "trapezoid", "a": a, "b": b, "h": h}
    print("Отправляем запрос серверу:", req)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cli:
        cli.settimeout(TIMEOUT)
        cli.connect((HOST, PORT))
        cli.sendall((json.dumps(req) + "\n").encode(ENC))

        data = cli.recv(BUF)
        if not data:
            print("Пустой ответ от сервера")
            return
        resp = json.loads(data.decode(ENC).strip())
        if resp.get("status") == "ok":
            print(f"Результат: S = {resp['result']}")
        else:
            print("Ошибка от сервера:", resp.get("message"))

if __name__ == "__main__":
    main()
