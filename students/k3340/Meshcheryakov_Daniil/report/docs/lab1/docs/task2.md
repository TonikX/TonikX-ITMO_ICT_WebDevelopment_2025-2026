# Задание 2: TCP-клиент и сервер (математические операции)

## Условие
Реализовать клиентскую и серверную часть приложения.  
Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры.  
Сервер обрабатывает данные и возвращает результат клиенту.  

Варианты операций:
1. Теорема Пифагора  
2. Решение квадратного уравнения  
3. Площадь трапеции  
4. Площадь параллелограмма  

Требования:
- Использовать библиотеку `socket`.  
- Реализовать с помощью протокола *TCP*.  

---

## Код программы

### Сервер (server.py)

```python
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
```

### Клиент (client.py)

```python
import socket, json

HOST = "127.0.0.1"
PORT = 9998

MENU = '''
1) Теорема Пифагора
2) Квадратное уравнение
3) Площадь трапеции
4) Площадь параллелограмма
Выберите операцию: 
'''

def main():
    op = input(MENU).strip().lower()
    params = {}
    if op in ("1","pythagoras"):
        params["a"] = input("a = ")
        params["b"] = input("b = ")
    elif op in ("2","quadratic"):
        params["a"] = input("a = ")
        params["b"] = input("b = ")
        params["c"] = input("c = ")
    elif op in ("3","trapezoid_area"):
        params["a"] = input("a = ")
        params["b"] = input("b = ")
        params["h"] = input("h = ")
    elif op in ("4","parallelogram_area"):
        params["a"] = input("a = ")
        params["h"] = input("h = ")
    else:
        print("Неизвестная операция")
        return

    req = {"operation": op, "params": params}
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(json.dumps(req).encode("utf-8"))
        data = s.recv(4096)
        print("Ответ:", data.decode("utf-8"))

if __name__ == "__main__":
    main()
```

---

## Запуск

1. Открыть два терминала.  
2. В первом запустить сервер:  
   ```bash
   python server.py
   ```
3. Во втором запустить клиента:  
   ```bash
   python client.py
   ```

---

## Результат

**Пример 1. Теорема Пифагора (a=3, b=4):**
```
Ответ: {"operation": "pythagoras", "a": 3.0, "b": 4.0, "c": 5.0}
```

**Пример 2. Квадратное уравнение (a=1, b=-3, c=2):**
```
Ответ: {"D": 1.0, "roots": [2.0, 1.0]}
```

**Пример 3. Площадь трапеции (a=3, b=5, h=4):**
```
Ответ: {"area": 16.0}
```

**Пример 4. Площадь параллелограмма (a=6, h=3):**
```
Ответ: {"area": 18.0}
```

---

## Выводы

1. Реализован клиент и сервер для вычисления математических задач через TCP-соединение.  
2. Используется передача данных в формате JSON.  
3. Поддерживаются четыре типа операций.  
4. Для каждого клиента создаётся отдельный поток на сервере, что позволяет обрабатывать несколько запросов одновременно.
