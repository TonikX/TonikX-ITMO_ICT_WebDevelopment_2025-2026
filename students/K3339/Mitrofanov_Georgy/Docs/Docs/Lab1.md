# Лабораторная работа №1

**Студент:** Митрофанов Георгий Алексеевич  
**Университет:** ИТМО  
**Группа:** К3339 

---

## Содержание

1. [Задание 1 (UDP)](#задание-1-udp)
2. [Задание 2 (TCP)](#задание-2-tcp)
3. [Задание 3 (HTTP)](#задание-3-http)
4. [Задание 4 (Многопользовательский чат)](#задание-4-многопользовательский-чат)
5. [Задание 5 (Web-сервер)](#задание-5-web-сервер)

---

## Задание 1 (UDP)<a id="задание-1-udp"></a>

### Условие
Реализовать клиентскую и серверную часть приложения. Клиент отправляет серверу сообщение «Hello, server», и оно должно отобразиться на стороне сервера. В ответ сервер отправляет клиенту сообщение «Hello, client», которое должно отобразиться у клиента.

### Требования
- Использовать библиотеку `socket`.
- Реализовать обмен с помощью протокола UDP.

### Код:

Server.py:
```python
import socket

# Сервер слушает конкретный IP и порт
HOST = "127.0.0.1"
PORT = 9999

# AF_INET = IPv4, SOCK_DGRAM = UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# bind = "занять" адрес/порт, чтобы принимать UDP-пакеты
server_socket.bind((HOST, PORT))

print(f"UDP server started on {HOST}:{PORT}")
print("Waiting for message...")

while True:
    # recvfrom возвращает (данные, адрес_клиента)
    data, client_addr = server_socket.recvfrom(4096)

    # UDP присылает байты, переводим в строку
    message = data.decode("utf-8")
    print(f"Received from {client_addr}: {message}")

    # Отправляем ответ туда же (на адрес клиента)
    reply = "Hello, client"
    server_socket.sendto(reply.encode("utf-8"), client_addr)
    print(f"Sent to {client_addr}: {reply}")
```

Client.py:
```python
import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9999

# Создаем UDP-сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Отправляем сообщение серверу
message = "Hello, server"
client_socket.sendto(message.encode("utf-8"), (SERVER_HOST, SERVER_PORT))
print(f"Sent to server: {message}")

# Ждём ответ от сервера
data, addr = client_socket.recvfrom(4096)
reply = data.decode("utf-8")
print(f"Received from server {addr}: {reply}")

# Закрываем сокет, освобождаем ресурсы
client_socket.close()
```

### Суть работы 
- Разработан UDP-клиент и сервер, которые обмениваются сообщениями. Клиент отправляет сообщение серверу, сервер его принимает и отвечает обратно. Основная цель - показать работу протокола UDP и обмен данными без установления соединения.

### Клиент
![1](img/Lab1/1.png)

### Сервер
![2](img/Lab1/2.png)


## Задание 2 (TCP) <a id="задание-2-tcp"></a>

### Условие
Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.  
Вариан - Множество операций (теорема Пифагора, квадратное уравнение, площадь трапеции, площадь параллелограмма)
### Требования
- Использовать библиотеку `socket`.
- Реализовать обмен с помощью протокола TCP.

### Код:

server.py:
```python
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
```

client.py:
```python
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
```

### Суть работы 
- Разработан TCP-клиент и сервер для нахождения корней уравнения. Клиент отправляет серверу три числа (коэффициенты a, b, c), сервер вычисляет корни и возвращает результат.

### Клиент
![3](img/Lab1/3.png)

### Сервер
![4](img/Lab1/4.png)

---

## Задание 3 (HTTP) <a id="задание-3-http"></a>

### Условие
Реализовать серверную часть приложения. Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, которая сервер подгружает из файла index.html.

### Требования
- Использовать библиотеку `socket`.

### Код:

index.html:
```html
<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8" />
  <title>Task 3</title>
</head>
<body>
  <h1>Добрый вечер!</h1>
  <p>Здесь что-то было, но по личным соображениям решило покинуть это место</p>
</body>
</html>

```

Server.py:
```python
import socket
from pathlib import Path

HOST = "127.0.0.1"
PORT = 8080

INDEX_PATH = Path(__file__).with_name("index.html")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"HTTP server started on http://{HOST}:{PORT}/")

def build_response(body: bytes, status: str = "200 OK", content_type: str = "text/html; charset=utf-8") -> bytes:
    headers = [
        f"HTTP/1.1 {status}",
        f"Content-Type: {content_type}",
        f"Content-Length: {len(body)}",
        "Connection: close",
        "",
        ""
    ]
    return ("\r\n".join(headers)).encode("utf-8") + body

while True:
    conn, addr = server_socket.accept()
    try:
        request_data = conn.recv(4096).decode("utf-8", errors="ignore")
        first_line = request_data.splitlines()[0] if request_data else ""
        print(f"Request from {addr}: {first_line}")

        if INDEX_PATH.exists():
            # Читаем HTML и добавляем CSS стили
            html_content = INDEX_PATH.read_text(encoding="utf-8")
            
            # Добавляем стили, если их нет
            if "<style>" not in html_content:
                styled_html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <title>Моя страница</title>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            max-width: 800px;
                            margin: 50px auto;
                            padding: 20px;
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            color: white;
                            border-radius: 10px;
                            box-shadow: 0 0 20px rgba(0,0,0,0.3);
                        }}
                        h1 {{
                            text-align: center;
                            border-bottom: 2px solid white;
                            padding-bottom: 10px;
                        }}
                        p {{
                            line-height: 1.6;
                            font-size: 18px;
                        }}
                    </style>
                </head>
                <body>
                    {html_content}
                </body>
                </html>
                """
                html = styled_html.encode("utf-8")
            else:
                html = INDEX_PATH.read_bytes()
            
            resp = build_response(html, "200 OK")
        else:
            body = b"""
            <html>
            <head><title>404 Not Found</title></head>
            <body style="font-family: Arial; text-align: center; padding: 50px;">
                <h1 style="color: #ff4444;">404</h1>
                <p>index.html not found</p>
                <hr>
                <small>HTTP Server v2.0</small>
            </body>
            </html>
            """
            resp = build_response(body, "404 Not Found")

        conn.sendall(resp)
    finally:
        conn.close()
```

### Суть работы
Разработан HTTP-сервер на Python с использованием сокетов. Сервер принимает запросы от клиента, загружает HTML-файл index.html и возвращает его браузеру в виде HTTP-ответа.

### Скриншоты работы
![5](img/Lab1/5.png)
![6](img/Lab1/6.png)
---

## Задание 4 (Многопользовательский чат) <a id="задание-4-многопользовательский-чат"></a>

### Условие
Реализовать двухпользовательский или многопользовательский чат. Клиенты подключаются к серверу и обмениваются сообщениями через сервер.

### Требования
- Обязательно использовать библиотеку `socket`.
- Для многопользовательского чата использовать библиотеку `threading`.
- Протокол TCP — 100% баллов; UDP — 80% (для UDP использовать потоки для приёма сообщений).

### Код:

Server.py:
```python
import socket
import threading

clients = []
nicknames = []


def start_server(host="localhost", port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Сервер запущен на {host}:{port}")

    while True:
        client_socket, address = server_socket.accept()
        print(f"Подключение от {address}")

        client_socket.send("NICK".encode("utf-8"))
        nickname = client_socket.recv(1024).decode("utf-8")

        nicknames.append(nickname)
        clients.append(client_socket)

        print(f"Никнейм клиента: {nickname}")
        broadcast(
            f"{nickname} присоединился к чату!".encode("utf-8"),
            client_socket,
            is_notif=True,
        )

        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()


def broadcast(message, client_socket, is_notif=False):
    response = ""
    for client in clients:
        if client != client_socket:
            if is_notif:
                response = message
            else:
                index = clients.index(client_socket)
                nickname = nicknames[index]
                response = f"\r{nickname} : ".encode("utf-8") + message
            try:
                client.send(response)
            except:
                remove_client(client)


def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                broadcast(message, client_socket)
            else:
                remove_client(client_socket)
                break
        except:
            remove_client(client_socket)
            break


def remove_client(client_socket):
    if client_socket in clients:
        index = clients.index(client_socket)
        nickname = nicknames[index]

        clients.remove(client_socket)
        nicknames.remove(nickname)

        broadcast(
            f"{nickname} покинул чат".encode("utf-8"), client_socket, is_notif=True
        )
        client_socket.close()


if __name__ == "__main__":
    start_server()
```

client.py:
```python
import socket
import threading


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            print(message)
        except:
            print("Соединение разорвано!")
            client_socket.close()
            break


def start_client(host="localhost", port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))

        nickname_request = client_socket.recv(1024).decode("utf-8")
        if nickname_request == "NICK":
            nickname = input("Введите ваш никнейм: ")
            client_socket.send(nickname.encode("utf-8"))

        receive_thread = threading.Thread(
            target=receive_messages, args=(client_socket,)
        )
        receive_thread.daemon = True
        receive_thread.start()

        while True:
            print(f"{nickname} : ", end="")
            message = input()
            if message.lower() == "quit":
                client_socket.close()
                break
            try:
                client_socket.send(message.encode("utf-8"))
            except:
                print("Ошибка отправки сообщения!")
                break

    except Exception as e:
        print(f"Ошибка подключения: {e}")
    finally:
        client_socket.close()


if __name__ == "__main__":
    start_client()
```

### Суть работы
Разработан многопользовательский чат на TCP с использованием потоков (threading). Сервер обрабатывает подключения нескольких клиентов одновременно, пересылая сообщения всем остальным пользователям. Клиент может одновременно получать и отправлять сообщения. 


## Задание 5 (Web-сервер) <a id="задание-5-web-сервер"></a>

### Условие
Написать простой веб‑сервер на Python с использованием `socket`, который:
- принимает и записывает информацию о дисциплине и оценке (POST),
- возвращает HTML‑страницу со всеми оценками (GET).

### Требования
- Использовать библиотеку `socket`.

### Код:

Server.py:
```python
import socket
from pathlib import Path
import urllib.parse
import json

HOST = "127.0.0.1"
PORT = 8081

DATA_PATH = Path(__file__).with_name("journal.json")

def load_journal() -> dict:
    if not DATA_PATH.exists():
        return {}
    try:
        return json.loads(DATA_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}

def save_journal(journal: dict) -> None:
    DATA_PATH.write_text(json.dumps(journal, ensure_ascii=False, indent=2), encoding="utf-8")

def http_response(body: str, status: str = "200 OK", content_type: str = "text/html; charset=utf-8") -> bytes:
    body_bytes = body.encode("utf-8")
    headers = [
        f"HTTP/1.1 {status}",
        f"Content-Type: {content_type}",
        f"Content-Length: {len(body_bytes)}",
        "Connection: close",
        "",
        ""
    ]
    return ("\r\n".join(headers)).encode("utf-8") + body_bytes

def parse_http_request(conn: socket.socket) -> tuple:
    data = b""
    while b"\r\n\r\n" not in data:
        chunk = conn.recv(4096)
        if not chunk:
            break
        data += chunk

    header_part, _, rest = data.partition(b"\r\n\r\n")
    header_text = header_part.decode("utf-8", errors="ignore")
    lines = header_text.split("\r\n")

    if not lines or len(lines[0].split()) < 2:
        return "", "", {}, b""

    request_line = lines[0]
    method, path = request_line.split()[0], request_line.split()[1]

    headers = {}
    for line in lines[1:]:
        if ":" in line:
            k, v = line.split(":", 1)
            headers[k.strip().lower()] = v.strip()

    body = rest
    if method.upper() == "POST":
        content_length = int(headers.get("content-length", "0"))
        while len(body) < content_length:
            chunk = conn.recv(4096)
            if not chunk:
                break
            body += chunk
        body = body[:content_length]

    return method.upper(), path, headers, body

def render_page(journal: dict) -> str:
    """Современный дизайн с карточками и градиентами"""
    cards = ""
    for subject, grades in journal.items():
        grades_list = [str(g) for g in grades]
        grades_str = ", ".join(grades_list)
        avg = sum(grades) / len(grades) if grades else 0
        cards += f"""
        <div class="subject-card">
            <div class="subject-header">{subject}</div>
            <div class="grades-container">
                <span class="grades-label">Оценки:</span>
                <span class="grades-list">{grades_str}</span>
            </div>
            <div class="stats">
                <div class="stat-item">
                    <span class="stat-label">Всего оценок:</span>
                    <span class="stat-value">{len(grades)}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Средний балл:</span>
                    <span class="stat-value">{avg:.2f}</span>
                </div>
            </div>
        </div>
        """

    if not cards:
        cards = '<div class="empty-state">📝 Пока нет оценок. Добавьте первую!</div>'

    return f"""<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8" />
  <title>📚 Электронный журнал</title>
  <style>
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    body {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        padding: 20px;
    }}
    .container {{
        max-width: 1200px;
        margin: 0 auto;
    }}
    .header {{
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 30px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }}
    h1 {{
        color: #333;
        font-size: 2.5em;
        margin-bottom: 20px;
        border-left: 5px solid #667eea;
        padding-left: 20px;
    }}
    .form-container {{
        background: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
    }}
    h2 {{
        color: #555;
        margin-bottom: 20px;
        font-size: 1.5em;
    }}
    .form-group {{
        margin-bottom: 15px;
    }}
    label {{
        display: block;
        margin-bottom: 5px;
        color: #666;
        font-weight: 500;
    }}
    input {{
        width: 100%;
        padding: 10px;
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        font-size: 16px;
        transition: border-color 0.3s;
    }}
    input:focus {{
        outline: none;
        border-color: #667eea;
    }}
    button {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 8px;
        font-size: 16px;
        cursor: pointer;
        transition: transform 0.2s;
    }}
    button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }}
    .subjects-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 20px;
        margin-top: 30px;
    }}
    .subject-card {{
        background: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }}
    .subject-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }}
    .subject-header {{
        font-size: 1.3em;
        font-weight: bold;
        color: #333;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 2px solid #667eea;
    }}
    .grades-container {{
        margin-bottom: 15px;
    }}
    .grades-label {{
        color: #666;
        font-weight: 500;
    }}
    .grades-list {{
        color: #333;
        font-weight: bold;
    }}
    .stats {{
        display: flex;
        justify-content: space-between;
        background: #f8f9fa;
        padding: 10px;
        border-radius: 8px;
        margin-top: 10px;
    }}
    .stat-item {{
        text-align: center;
    }}
    .stat-label {{
        display: block;
        font-size: 0.8em;
        color: #888;
    }}
    .stat-value {{
        font-size: 1.2em;
        font-weight: bold;
        color: #667eea;
    }}
    .empty-state {{
        grid-column: 1 / -1;
        text-align: center;
        padding: 50px;
        background: white;
        border-radius: 15px;
        font-size: 1.2em;
        color: #888;
    }}
    .footer {{
        text-align: center;
        margin-top: 30px;
        color: rgba(255,255,255,0.8);
        font-size: 0.9em;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>📋 Электронный журнал успеваемости</h1>
      
      <div class="form-container">
        <h2>➕ Добавить новую оценку</h2>
        <form method="POST" action="/">
          <div class="form-group">
            <label>Название дисциплины:</label>
            <input name="subject" placeholder="Например: Математика" required>
          </div>
          <div class="form-group">
            <label>Оценка (1-5):</label>
            <input name="grade" type="number" min="1" max="5" placeholder="5" required>
          </div>
          <button type="submit">💾 Сохранить оценку</button>
        </form>
      </div>
    </div>

    <h2 style="color: white;">📊 Текущие оценки</h2>
    <div class="subjects-grid">
      {cards}
    </div>
    
    <div class="footer">
      Данные хранятся в файле journal.json | Обновлено: {__import__('datetime').datetime.now().strftime('%d.%m.%Y %H:%M')}
    </div>
  </div>
</body>
</html>
"""

def is_valid_grade(grade_str: str) -> bool:
    try:
        g = int(grade_str)
        return 1 <= g <= 5
    except ValueError:
        return False

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(10)

print(f"Journal HTTP server started on http://{HOST}:{PORT}/")

while True:
    conn, addr = server_socket.accept()
    try:
        method, path, headers, body = parse_http_request(conn)
        journal = load_journal()

        if method == "GET":
            page = render_page(journal)
            conn.sendall(http_response(page))

        elif method == "POST":
            form = urllib.parse.parse_qs(body.decode("utf-8", errors="ignore"))

            subject = (form.get("subject", [""])[0]).strip()
            grade = (form.get("grade", [""])[0]).strip()

            if not subject or not grade or not is_valid_grade(grade):
                page = "<h1>400 Bad Request</h1><p>Нужно передать subject и grade (оценка 1..5).</p>"
                conn.sendall(http_response(page, status="400 Bad Request"))
            else:
                journal.setdefault(subject, [])
                journal[subject].append(int(grade))
                save_journal(journal)

                page = render_page(journal)
                conn.sendall(http_response(page))

        else:
            conn.sendall(http_response("<h1>405 Method Not Allowed</h1>", status="405 Method Not Allowed"))

    except Exception as e:
        conn.sendall(http_response(f"<h1>500</h1><pre>{e}</pre>", status="500 Internal Server Error"))
    finally:
        conn.close()
```

### Суть работы
Разработан простой веб-сервер на Python с обработкой GET и POST запросов. Сервер принимает данные о дисциплине и оценке, сохраняет их и возвращает HTML-страницу со списком всех оценок.

### Скриншоты работы
![7](img/Lab1/7.png)
---

## Вывод <a id="вывод"></a>
В ходе лабораторной работы №1 были изучены и реализованы различные сетевые приложения на Python с использованием библиотеки socket: обмен сообщениями по UDP, клиент-серверные вычисления по TCP, работа HTTP-сервера с HTML-страницами, многопользовательский чат и веб-сервер с обработкой GET и POST-запросов. Работа позволила закрепить практические навыки работы с протоколами UDP, TCP, потоками, HTTP и передачей данных между клиентом и сервером.