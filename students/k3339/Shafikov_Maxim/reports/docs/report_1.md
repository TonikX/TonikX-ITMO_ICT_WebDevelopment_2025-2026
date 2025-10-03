# Отчет по лабораторной работе №1

**Выполнил:** Шафиков Максим Азатович 

**Факультет:** ПИН (ИКТ)

**Группа:** К3339  

**Преподаватель:** Говоров Антон Игоревич  

---

## Задание 1

**Задача:**  
Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.  
Протокол: **UDP**.  

**Решение:**  
Для решения задачи был использован модуль `socket`.  
Сервер создаёт UDP-сокет, принимает сообщения и отправляет ответ.  
Клиент создаёт UDP-сокет, отправляет строку «Hello, server» и получает от сервера «Hello, client».  

**Код:**  

server.py:
```python
import socket
from students.k3339.Shafikov_Maxim.Lr1.config import host, port

if __name__ == '__main__':
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((host, port))
    print(f"Сервер запущен на {host}:{port}")

    while True:
        data, addr = udp_socket.recvfrom(1024)
        message = data.decode("utf-8")
        print(f"Получено от {addr}: {message}")

        reply = "Hello, client"
        udp_socket.sendto(reply.encode("utf-8"), addr)
```

client.py:
```python
import socket
from students.k3339.Shafikov_Maxim.Lr1.config import host, port

if __name__ == '__main__':
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    message = "Hello, server"
    udp_socket.sendto(message.encode("utf-8"), (host, port))

    data, addr = udp_socket.recvfrom(1024)
    print(f"Ответ от сервера: {data.decode('utf-8')}")
```

---

## Задание 2

**Задача:**  
Клиент запрашивает выполнение математической операции (Теорема Пифагора).  
Сервер обрабатывает данные и возвращает результат клиенту.  
Протокол: **TCP**.  

**Решение:**  
Клиент запрашивает у пользователя катеты `a` и `b`. Отправляет их на сервер.  
Сервер принимает данные, вычисляет гипотенузу по формуле `c = sqrt(a^2 + b^2)` и возвращает клиенту.  

**Код:**  

client.py:
```python
import socket
from students.k3339.Shafikov_Maxim.Lr1.config import host, port

if __name__ == "__main__":
    a = input("Введите катет a: ")
    b = input("Введите катет b: ")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(f"{a} {b}".encode("utf-8"))
        data = s.recv(1024)

    print("Ответ сервера:", data.decode("utf-8"))
```

server.py:
```python
import socket
import math
from students.k3339.Shafikov_Maxim.Lr1.config import host, port

if __name__ == "__main__":
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind((host, port))
    tcp_socket.listen(5)
    print(f"Сервер слушает {host}:{port} (TCP)")

    while True:
        conn, addr = tcp_socket.accept()
        with conn:
            data = conn.recv(1024)
            if not data:
                continue
            try:
                a_str, b_str = data.decode("utf-8").split()
                a, b = float(a_str), float(b_str)
                c = math.sqrt(a*a + b*b)
                result = f"Гипотенуза c = {c}"
            except Exception as e:
                result = f"Ошибка: {e}"
            conn.sendall(result.encode("utf-8"))
```

---

## Задание 3

**Задача:**  
Сервер при подключении клиента отдаёт HTML-страницу из файла `index.html`.  

**Решение:**  
Был создан TCP-сервер, который слушает соединения и на любой запрос возвращает содержимое `index.html`.  
HTML-страница содержит кнопку и счётчик кликов.  

**Код:**  

index.html:
```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Кликер</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 100px; }
        button { font-size: 20px; padding: 10px 20px; }
        #count { font-size: 24px; margin-top: 20px; }
    </style>
</head>
<body>
    <h1>Клики</h1>
    <button id="btn">Клик</button>
    <div id="count">0</div>

    <script>
        const btn = document.getElementById("btn");
        const countDiv = document.getElementById("count");
        let count = 0;

        btn.addEventListener("click", () => {
            count++;
            countDiv.textContent = count;
        });
    </script>
</body>
</html>
```

server.py:
```python
import socket
import os
from students.k3339.Shafikov_Maxim.Lr1.config import host, port

if __name__ == "__main__":
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_socket.bind((host, port))
    tcp_socket.listen(5)

    print(f"Сервер запущен на http://{host}:{port}")

    while True:
        conn, addr = tcp_socket.accept()
        with conn:
            request = conn.recv(1024).decode("utf-8", errors="ignore")
            print(f"\n--- Запрос от {addr} ---")
            print(request)

            if os.path.exists("index.html"):
                with open("index.html", "r", encoding="utf-8") as f:
                    body = f.read()
                response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/html; charset=utf-8\r\n"
                    f"Content-Length: {len(body.encode('utf-8'))}\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                    f"{body}"
                )
            else:
                body = "<h1>Файл index.html не найден</h1>"
                response = (
                    "HTTP/1.1 404 Not Found\r\n"
                    "Content-Type: text/html; charset=utf-8\r\n"
                    f"Content-Length: {len(body.encode('utf-8'))}\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                    f"{body}"
                )

            conn.sendall(response.encode("utf-8"))
```

---

## Задание 4

**Задача:**  
Реализовать многопользовательский чат.  
Протокол: **TCP**.  
Необходимо сохранять пользователей и рассылать сообщения всем клиентам.  

**Решение:**  
Сервер обслуживает каждого клиента в отдельном потоке (через `threading`).  
Клиент сначала выбирает уникальный ник (сервер проверяет уникальность).  
Сообщения рассылаются всем пользователям, кроме отправителя.  

**Код:**  

server.py:
```python
import socket
import threading
from students.k3339.Shafikov_Maxim.Lr1.config import host, port

ENC = "utf-8"

# conn -> nickname
clients = {}
clients_lock = threading.Lock()


def send_line(conn, text: str):
    try:
        conn.sendall((text + "\n").encode(ENC))
    except OSError:
        pass


def broadcast(text: str, exclude=None):
    with clients_lock:
        dead = []
        for c in list(clients.keys()):
            if c is exclude:
                continue
            try:
                c.sendall((text + "\n").encode(ENC))
            except OSError:
                dead.append(c)
        for d in dead:
            name = clients.pop(d, None)
            try:
                d.close()
            except OSError:
                pass


def handle_client(conn: socket.socket, addr):
    name = None
    try:
        f = conn.makefile("r", encoding=ENC, newline="\n")

        # Выбор ника
        while True:
            send_line(conn, "Введите ник: ")
            name_line = f.readline()
            if not name_line:
                return
            candidate = name_line.strip()
            if not candidate:
                send_line(conn, "❌ Ник не может быть пустым.")
                continue
            with clients_lock:
                if candidate in clients.values():
                    send_line(conn, "❌ Ник уже занят. Попробуйте другой.")
                else:
                    name = candidate
                    clients[conn] = name
                    break

        send_line(conn, f"✅ Добро пожаловать, {name}! Напишите /quit для выхода.")
        broadcast(f"🟢 {name} присоединился к чату.", exclude=None)

        for line in f:
            msg = line.rstrip("\n")
            if not msg:
                continue
            if msg.strip().lower() == "/quit":
                send_line(conn, "Пока! Вы вышли из чата.")
                break
            broadcast(f"[{name}]: {msg}", exclude=conn)

    except Exception:
        pass
    finally:
        with clients_lock:
            if conn in clients:
                left_name = clients.pop(conn)
                broadcast(f"🔴 {left_name} покинул чат.", exclude=None)
        try:
            conn.close()
        except OSError:
            pass


def main():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_socket.bind((host, port))
    tcp_socket.listen()
    print(f"Сервер запущен на {host}:{port}")

    try:
        while True:
            conn, addr = tcp_socket.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("\nОстановка сервера...")
    finally:
        tcp_socket.close()


if __name__ == "__main__":
    main()
```

client.py:
```python
import socket
import threading
from students.k3339.Shafikov_Maxim.Lr1.config import host, port


def recv_loop(sock: socket.socket):
    """Фоновый поток для приёма сообщений после входа в чат."""
    try:
        f = sock.makefile("r", encoding="utf-8", newline="\n")
        for line in f:
            print(line.rstrip("\n"))
    except Exception:
        pass
    finally:
        try:
            sock.close()
        except OSError:
            pass


def main():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((host, port))
    f = tcp_socket.makefile("r", encoding="utf-8", newline="\n")

    # Выбор ника
    while True:
        prompt = f.readline()
        if not prompt:
            print("Сервер закрыл соединение.")
            return
        print(prompt.strip())
        name = input("> ")
        tcp_socket.sendall((name + "\n").encode("utf-8"))
        reply = f.readline()
        if not reply:
            print("Сервер закрыл соединение.")
            return
        print(reply.strip())
        if reply.startswith("✅"):
            break

    t = threading.Thread(target=recv_loop, args=(tcp_socket,), daemon=True)
    t.start()

    try:
        while True:
            line = input()
            if not line:
                continue
            tcp_socket.sendall((line + "\n").encode("utf-8"))
            if line.strip().lower() == "/quit":
                break
    except KeyboardInterrupt:
        tcp_socket.sendall(("/quit\n").encode("utf-8"))
    finally:
        try:
            tcp_socket.close()
        except OSError:
            pass


if __name__ == "__main__":
    main()
```

---

## Задание 5

**Задача:**  
Написать веб-сервер, который принимает и записывает информацию о дисциплине и оценке по дисциплине.  
Сервер должен отдать HTML-страницу с таблицей всех оценок.  

**Решение:**  
Использован TCP-сокет.  
- GET-запрос возвращает HTML-страницу с таблицей и формой для ввода.  
- POST-запрос добавляет запись (дисциплина + оценка), проверяет корректность, и снова отдаёт страницу.  
- Для дисциплин выводится список оценок и среднее значение.  

**Код:**  

server.py:
```python
import socket
import urllib.parse
from collections import defaultdict
from students.k3339.Shafikov_Maxim.Lr1.config import host, port


grades = defaultdict(list)


def render_html():
    rows = ""
    if grades:
        for subj, marks in grades.items():
            avg = sum(marks) / len(marks)
            marks_str = ", ".join(str(m) for m in marks)
            rows += f"<tr><td>{subj}</td><td>{marks_str}</td><td>{avg:.2f}</td></tr>\n"
    else:
        rows = '<tr><td colspan="3">Пока нет оценок</td></tr>'

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>Оценки по дисциплинам</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 40px; }}
    table {{ border-collapse: collapse; width: 500px; margin-bottom: 20px; }}
    th, td {{ border: 1px solid #333; padding: 8px; text-align: center; }}
    th {{ background: #eee; }}
    form {{ display: flex; flex-direction: column; width: 400px; gap: 10px; }}
    label {{ display: flex; justify-content: space-between; }}
    input[type=text], input[type=number] {{ flex: 1; margin-left: 10px; }}
    input[type=submit] {{ padding: 8px; font-size: 16px; }}
  </style>
</head>
<body>
  <h1>Оценки по дисциплинам</h1>
  <table>
    <tr><th>Дисциплина</th><th>Оценки</th><th>Средняя</th></tr>
    {rows}
  </table>
  <form method="POST">
    <label>Дисциплина: <input type="text" name="subject" required></label>
    <label>Оценка (1-5): <input type="number" name="grade" min="1" max="5" required></label>
    <input type="submit" value="Добавить">
  </form>
</body>
</html>"""


def handle_request(request: str):
    lines = request.split("\r\n")
    if not lines:
        return "HTTP/1.1 400 Bad Request\r\n\r\n"

    first_line = lines[0]
    method, *_ = first_line.split()

    if method == "POST":
        body = request.split("\r\n\r\n", 1)[-1]
        data = urllib.parse.parse_qs(body)
        subject = data.get("subject", [""])[0].strip()
        grade_str = data.get("grade", [""])[0].strip()

        if subject and grade_str.isdigit():
            grade = int(grade_str)
            if 1 <= grade <= 5:
                grades[subject].append(grade)

    body = render_html()
    headers = [
        "HTTP/1.1 200 OK",
        "Content-Type: text/html; charset=utf-8",
        f"Content-Length: {len(body.encode("utf-8"))}",
        "Connection: close",
        "",
        ""
    ]
    return "\r\n".join(headers) + body


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
        tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_socket.bind((host, port))
        tcp_socket.listen(5)
        print(f"Сервер слушает на http://{host}:{port}")

        while True:
            conn, addr = tcp_socket.accept()
            print(f"[+] Подключение от {addr[0]}:{addr[1]}")
            with conn:
                request = conn.recv(4096).decode("utf-8", errors="ignore")
                if not request:
                    continue
                response = handle_request(request)
                conn.sendall(response.encode("utf-8"))


if __name__ == "__main__":
    main()
```

---

## Вывод

В ходе выполнения лабораторной работы №1 были изучены основы работы с сетью на Python с помощью библиотеки `socket`.  
Реализованы:  
- UDP-сервер и клиент (обмен сообщениями).  
- TCP-сервер и клиент (математические вычисления).  
- Мини-веб-сервер, отдающий HTML-страницу.  
- Многопользовательский чат с потоками.  
- Веб-сервер для обработки GET/POST-запросов с сохранением и отображением данных.  

Работа позволила закрепить понимание различий между протоколами **UDP и TCP**, научиться обрабатывать сетевые соединения и реализовывать простейшие серверные приложения.  
