# Задание 2: TCP Математический Сервер

## Практическое задание

Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

**Варианты операций:**
- Теорема Пифагора
- Решение квадратного уравнения
- Поиск площади трапеции
- Поиск площади параллелограмма

**Порядок выбора варианта:** Выбирается по порядковому номеру в журнале (пятый студент получает вариант 1 и т.д.).

### Требования:
- Обязательно использовать библиотеку `socket`
- Реализовать с помощью протокола **TCP**

---

## Реализация

### Сервер (task2/server.py)

```python
import socket
import json
import math

HOST = '127.0.0.1'
PORT = 8002
ENCODING = 'utf-8'

def solve_quadratic(a, b, c):
    if a == 0:
        raise ValueError("a не должно быть 0")
    
    disc = b*b - 4*a*c
    if disc < 0:
        return "Нет действительных корней"
    elif disc == 0:
        x = -b / (2*a)
        return f"Один корень: x = {x:.2f}"
    else:
        sqrt_d = math.sqrt(disc)
        x1 = (-b + sqrt_d) / (2*a)
        x2 = (-b - sqrt_d) / (2*a)
        return f"Два корня: x1 = {x1:.2f}, x2 = {x2:.2f}"

def handle_request(data):
    try:
        req = json.loads(data)
        params = req.get("params", [])
        if len(params) != 3:
            raise ValueError("Нужны 3 параметра: a, b, c")
        
        a, b, c = map(float, params)
        result = solve_quadratic(a, b, c)
        return json.dumps({"status": "ok", "result": result}) + "\n"
    except Exception as e:
        return json.dumps({"status": "error", "error": str(e)}) + "\n"

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"TCP сервер квадратных уравнений на {HOST}:{PORT}")
        try:
            while True:
                conn, addr = s.accept()
                with conn:
                    print(f"Подключен: {addr}")

                    request = ""
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        request += data.decode(ENCODING)
                        if "\n" in request:
                            break
                    
                    response = handle_request(request.strip())
                    conn.sendall(response.encode(ENCODING))
        except KeyboardInterrupt:
            print("\nСервер завершает работу.")

if __name__ == '__main__':
    main()
```

### Клиент (task2/client.py)

```python
import socket
import json

HOST = '127.0.0.1'
PORT = 8002
ENCODING = 'utf-8'

def main():
    print("Решение квадратного уравнения ax² + bx + c = 0")
    params = input("Введите коэффициенты a b c через пробел: ").split()
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall((json.dumps({"params": params}) + "\n").encode(ENCODING))
        response = ""
        while True:
            data = s.recv(1024)
            if not data:
                break
            response += data.decode(ENCODING)
            if "\n" in response:
                break
        
        resp = json.loads(response.strip())
        if resp.get("status") == "ok":
            print("Результат:", resp["result"])
        else:
            print("Ошибка:", resp.get("error"))

if __name__ == '__main__':
    main()
```

## Запуск

1. Откройте два терминала
2. В первом запустите сервер:
   ```bash
   python task2/server.py
   ```
3. Во втором запустите клиент:
   ```bash
   python task2/client.py
   ```

## Результат

**Сервер:**
```
TCP сервер квадратных уравнений на 127.0.0.1:8002
Подключен: ('127.0.0.1', 54321)
```

**Клиент:**
```
Решение квадратного уравнения ax² + bx + c = 0
Введите коэффициенты a b c через пробел: 1 -5 6
Результат: Два корня: x1 = 3.00, x2 = 2.00
```

## Выводы

1. Реализован TCP сервер для решения квадратных уравнений
2. Использована JSON сериализация для передачи данных
3. Добавлена обработка ошибок и валидация входных данных
4. TCP обеспечивает надежную доставку данных