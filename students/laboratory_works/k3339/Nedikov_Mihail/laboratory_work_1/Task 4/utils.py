import json


def recv_json(conn):
    """Принимает префикс длины и возвращает JSON-объект или None."""
    raw_len = conn.recv(4)
    if not raw_len:
        return None

    msg_len = int.from_bytes(raw_len, "big")
    data = b""
    while len(data) < msg_len:
        packet = conn.recv(msg_len - len(data))
        if not packet:
            return None
        data += packet
    return json.loads(data.decode("utf-8"))


def send_json(conn, obj):
    """Сериализует объект в JSON и отправляет его с длиной в префиксе."""
    data = json.dumps(obj).encode("utf-8")
    conn.sendall(len(data).to_bytes(4, "big") + data)
