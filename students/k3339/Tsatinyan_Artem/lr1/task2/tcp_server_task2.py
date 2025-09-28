import socket
import json

HOST = "127.0.0.1"
PORT = 9090
ENC = "utf-8"
BUF = 4096

def compute_trapezoid(a: float, b: float, h: float) -> float:
    if h < 0:
        raise ValueError("высота (h) должна быть неотрицательна")
    if a < 0 or b < 0:
        raise ValueError("основания (a, b) должны быть неотрицательны")
    return (a + b) * 0.5 * h

def handle_request(raw: str) -> dict:
    try:
        payload = json.loads(raw)

        op = payload.get("op")
        if op != "trapezoid":
            raise ValueError("Неподдерживаемый op")

        a = float(payload.get("a"))
        b = float(payload.get("b"))
        h = float(payload.get("h"))

        result = compute_trapezoid(a, b, h)
        return {"status": "ok", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORT))
        srv.listen(5)
        while True:
            conn, addr = srv.accept()
            with conn:
                try:
                    data = conn.recv(BUF)
                    if not data:
                        continue
                    raw = data.decode(ENC, errors="replace").strip()
                    print(f"Получено от {addr}: {raw}")
                    resp = handle_request(raw)
                    payload = (json.dumps(resp) + "\n").encode(ENC)
                    conn.sendall(payload)
                except Exception as e:
                    err = {"status":"error","message":f"internal error: {e}"}
                    conn.sendall((json.dumps(err) + "\n").encode(ENC))

if __name__ == "__main__":
    main()
