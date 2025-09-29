# Задание 3: HTTP-сервер и HTML-страница

## Условие
Реализовать серверную часть приложения.  
Клиент подключается к серверу, и в ответ получает HTTP-сообщение, содержащее HTML-страницу, загружаемую из файла `index.html`.  

Требования:
- Использовать библиотеку `socket`.  
- Протокол: *TCP (HTTP поверх TCP)*.  

---

## Код программы

### Сервер (server.py)

```python
import socket
import os

HOST = "127.0.0.1"
PORT = 8080
INDEX = "index.html"

def build_response(status, body):
    body_bytes = body if isinstance(body, bytes) else body.encode("utf-8")
    headers = f"HTTP/1.1 {status}\r\nContent-Length: {len(body_bytes)}\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
    return headers.encode("utf-8") + body_bytes

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"[HTTP SERVER] http://{HOST}:{PORT}")
        while True:
            conn, _ = s.accept()
            with conn:
                conn.recv(1024)
                if os.path.exists(INDEX):
                    with open(INDEX, "rb") as f:
                        body = f.read()
                    resp = build_response("200 OK", body)
                else:
                    resp = build_response("404 Not Found", "<h1>404</h1>")
                conn.sendall(resp)

if __name__ == "__main__":
    main()
```

### HTML-страница (index.html)

```html
<!DOCTYPE html>
<html lang="ru">
  <head>
    <meta charset="utf-8" />
    <title>Socket HTTP Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <style>
      body {
        margin: 0;
        font-family: "Segoe UI", Roboto, sans-serif;
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        color: #fff;
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
      }
      .card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(8px);
        border-radius: 16px;
        padding: 2rem 3rem;
        max-width: 600px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
        animation: fadeIn 1s ease;
      }
      h1 {
        margin-bottom: 1rem;
        font-size: 2.2rem;
        text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.4);
      }
      p {
        font-size: 1.2rem;
        margin: 0.5rem 0;
      }
      code {
        background: rgba(0, 0, 0, 0.5);
        padding: 0.2rem 0.5rem;
        border-radius: 6px;
        font-family: monospace;
      }
      .btn {
        display: inline-block;
        margin-top: 1.5rem;
        padding: 0.8rem 1.5rem;
        font-size: 1rem;
        color: #1e3c72;
        background: #fff;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
        transition: all 0.2s ease;
      }
      .btn:hover {
        background: #f1f1f1;
        transform: translateY(-2px);
      }
      @keyframes fadeIn {
        from {
          opacity: 0;
          transform: translateY(20px);
        }
        to {
          opacity: 1;
          transform: translateY(0);
        }
      }
    </style>
  </head>
  <body>
    <div class="card">
      <h1>Добро пожаловать!</h1>
      <p>Эта страница отдана простым <code>socket</code>-сервером на Python.</p>
      <p>Вроде красиво вышло</p>
      <a class="btn" href="https://www.python.org/">Вот ссылочка</a>
    </div>
  </body>
</html>
```

---

## Запуск

1. Запустить сервер:  
   ```bash
   python server.py
   ```
2. Открыть в браузере:  
   ```
   http://127.0.0.1:8080
   ```

---

## Результат

**Браузер отправляет:**
```
GET / HTTP/1.1
```

**Сервер отвечает:**
```
HTTP/1.1 200 OK
Content-Length: 1234
Content-Type: text/html; charset=utf-8
```

И отдаёт содержимое `index.html`.  
В браузере отображается стилизованная HTML-страница с карточкой, заголовком, текстом и кнопкой-ссылкой.  

---

## Выводы

1. Реализован простой HTTP-сервер на базе `socket`.  
2. Сервер обрабатывает запросы и отдаёт статический HTML-файл.  
3. При отсутствии файла отдаётся сообщение об ошибке `404`.  
4. HTML-страница дополнена CSS-стилями, что улучшает внешний вид результата.
