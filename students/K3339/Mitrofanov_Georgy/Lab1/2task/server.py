import socket
import json
import math

HOST = "127.0.0.1"
PORT = 9998

# TCP-сокет: SOCK_STREAM
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

# backlog = сколько подключений можно держать в очереди
server_socket.listen(5)

print(f"TCP math server started on {HOST}:{PORT}")


def handle_request(req: dict) -> dict:
    """Обрабатываем запрос от клиента и возвращаем результат."""
    op = req.get("op")

    # 1) Теорема Пифагора: c = sqrt(a^2 + b^2)
    if op == "pythagoras":
        a = float(req["a"])
        b = float(req["b"])
        c = math.sqrt(a * a + b * b)
        return {"ok": True, "result": c}

    # 2) Квадратное уравнение: ax^2 + bx + c = 0
    if op == "quadratic":
        a = float(req["a"])
        b = float(req["b"])
        c = float(req["c"])

        if a == 0:
            return {"ok": False, "error": "a не может быть 0 (это не квадратное уравнение)"}

        d = b * b - 4 * a * c  # дискриминант
        if d < 0:
            return {"ok": True, "result": [], "note": "Корней нет (D < 0)"}
        if d == 0:
            x = -b / (2 * a)
            return {"ok": True, "result": [x], "note": "Один корень (D = 0)"}

        sqrt_d = math.sqrt(d)
        x1 = (-b + sqrt_d) / (2 * a)
        x2 = (-b - sqrt_d) / (2 * a)
        return {"ok": True, "result": [x1, x2], "note": "Два корня (D > 0)"}

    # 3) Площадь трапеции: S = (a + b) / 2 * h
    if op == "trapezoid_area":
        a = float(req["a"])
        b = float(req["b"])
        h = float(req["h"])
        s = (a + b) / 2.0 * h
        return {"ok": True, "result": s}

    # 4) Площадь параллелограмма: S = a * h
    if op == "parallelogram_area":
        a = float(req["a"])
        h = float(req["h"])
        s = a * h
        return {"ok": True, "result": s}

    return {"ok": False, "error": "Неизвестная операция"}


def recv_line(conn: socket.socket) -> str:
    """Читаем данные до '\\n' (клиент шлёт JSON одной строкой)."""
    buf = b""
    while True:
        chunk = conn.recv(1)
        if not chunk:
            break
        if chunk == b"\n":
            break
        buf += chunk
    return buf.decode("utf-8")


while True:
    conn, addr = server_socket.accept()
    print(f"Client connected: {addr}")

    try:
        # Клиент шлёт JSON одной строкой + \n
        line = recv_line(conn)
        if not line:
            conn.close()
            continue

        req = json.loads(line)
        resp = handle_request(req)

        # Отправляем ответ тоже JSON-строкой
        conn.sendall((json.dumps(resp, ensure_ascii=False) + "\n").encode("utf-8"))

    except Exception as e:
        err = {"ok": False, "error": f"Ошибка на сервере: {e}"}
        conn.sendall((json.dumps(err, ensure_ascii=False) + "\n").encode("utf-8"))

    finally:
        conn.close()
        print(f"Client disconnected: {addr}")
