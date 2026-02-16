import socket
import json

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9998


def ask_float(prompt: str) -> float:
    # Просим число у пользователя, пока он не введёт нормально
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Введите число.")


def main():
    # Вариант 4: площадь параллелограмма
    # Формула: S = a * h
    a = ask_float("Введите сторону a: ")
    h = ask_float("Введите высоту h: ")

    # Готовим запрос для сервера (в JSON)
    req = {"op": "parallelogram_area", "a": a, "h": h}

    # Подключаемся к серверу по TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_HOST, SERVER_PORT))

        # Отправляем JSON в одну строку + \n
        s.sendall((json.dumps(req, ensure_ascii=False) + "\n").encode("utf-8"))

        # Читаем ответ (тоже до \n)
        data = b""
        while not data.endswith(b"\n"):
            chunk = s.recv(4096)
            if not chunk:
                break
            data += chunk

    # Разбираем JSON-ответ
    resp = json.loads(data.decode("utf-8").strip())

    if resp.get("ok"):
        print("Результат:", resp.get("result"))
        if "note" in resp:
            print("Комментарий:", resp["note"])
    else:
        print("Ошибка:", resp.get("error"))


if __name__ == "__main__":
    main()
