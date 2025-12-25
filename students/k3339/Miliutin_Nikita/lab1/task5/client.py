import socket

HOST = "localhost"   # IP сервера
PORT = 9090          # порт сервера (подставь свой)

def send_request(raw_request: str):
    """Отправить HTTP-запрос и вывести ответ"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(raw_request.encode("utf-8"))
        data = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            data += chunk
        response = data.decode("utf-8", errors="ignore")
        print("=== Ответ сервера ===")
        print(response)
        print("=====================")

# --- шаблоны запросов ---
get_request = (
    "GET / HTTP/1.1\r\n"
    f"Host: {HOST}\r\n"
    "Connection: close\r\n"
    "\r\n"
)

post_template = (
    "POST /?discipline={disc}&grade={grade} HTTP/1.1\r\n"
    f"Host: {HOST}\r\n"
    "Content-Length: 0\r\n"
    "Connection: close\r\n"
    "\r\n"
)

# --- список записей для добавления ---
grades_to_add = [
    ("Math", "5"),
    ("Physics", "4"),
    ("Programming", "A"),
    ("History", "B"),
    ("English", "C"),
    ("Databases", "90"),
    ("Networking", "Passed"),
    ("Algorithms", "Excellent"),
    ("PE", "OK"),
    ("Art", "A+")
]

# --- добавляем все записи ---
for disc, grade in grades_to_add:
    print(f"Отправляю POST-запрос: {disc}={grade}")
    send_request(post_template.format(disc=disc, grade=grade))

# --- в конце GET-запрос чтобы посмотреть таблицу ---
print("Отправляю GET-запрос чтобы посмотреть таблицу ...")
send_request(get_request)
