import socket
import threading
import json
import math

HOST = "127.0.0.1"
PORT = 9998

def pythagoras(params):
    a = float(params["a"]); b = float(params["b"])
    return {"operation":"pythagoras","a":a,"b":b,"c": (a*a + b*b) ** 0.5}

def quadratic(params):
    a = float(params["a"]); b = float(params["b"]); c = float(params["c"])
    if a == 0:
        if b == 0:
            return {"error":"a=0 and b=0 → нет решения"}
        return {"x": -c/b, "note":"линейное уравнение (a=0)"}
    D = b*b - 4*a*c
    if D < 0:
        return {"D":D,"roots":[],"note":"корней нет"}
    if D == 0:
        return {"D":D,"roots":[-b/(2*a)]}
    sqrtD = D ** 0.5
    return {"D":D,"roots":[(-b+sqrtD)/(2*a), (-b-sqrtD)/(2*a)]}

def trapezoid_area(params):
    a = float(params["a"]); b = float(params["b"]); h = float(params["h"])
    return {"area": (a+b)*0.5*h}

def parallelogram_area(params):
    a = float(params["a"]); h = float(params["h"])
    return {"area": a*h}

OPS = {
    "1": pythagoras,
    "2": quadratic,
    "3": trapezoid_area,
    "4": parallelogram_area,
    "pythagoras": pythagoras,
    "quadratic": quadratic,
    "trapezoid_area": trapezoid_area,
    "parallelogram_area": parallelogram_area,
}

def handle(conn):
    with conn:
        try:
            raw = conn.recv(4096)
            if not raw:
                return
            req = json.loads(raw.decode("utf-8"))
            op = str(req.get("operation","")).lower()
            fn = OPS.get(op)
            if not fn:
                resp = {"error":"Неизвестная операция"}
            else:
                resp = fn(req.get("params", {}))
            conn.sendall(json.dumps(resp, ensure_ascii=False).encode("utf-8"))
        except Exception as e:
            conn.sendall(json.dumps({"error": str(e)}).encode("utf-8"))

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"[TCP MATH SERVER] {HOST}:{PORT}")
        while True:
            conn, _ = s.accept()
            threading.Thread(target=handle, args=(conn,), daemon=True).start()

if __name__ == "__main__":
    main()
