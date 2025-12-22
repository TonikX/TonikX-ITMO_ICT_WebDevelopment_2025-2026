# Задание 4 - Многопользовательский чат

## Описание задания

Реализовать многопользовательский чат-сервер с поддержкой одновременных подключений нескольких клиентов. Сервер должен использовать многопоточность для обработки множественных соединений и рассылать сообщения от одного клиента всем остальным (broadcast).

## Теоретические основы

### Многопоточность (Threading)

**Многопоточность** позволяет:
- Одновременно обрабатывать несколько клиентов
- Не блокировать основной поток при работе с одним клиентом
- Эффективно использовать ресурсы процессора
- Реализовывать параллельные задачи

### Broadcast Messaging

**Broadcast** - рассылка сообщения всем подключенным клиентам:
- Один клиент отправляет сообщение серверу
- Сервер пересылает его всем активным клиентам
- Все участники видят сообщения друг друга

## Структура проекта

```
task4/
├── server.py          # Многопоточный чат-сервер
├── client.py          # Клиентское приложение
└── message_entity.py  # Структура данных для сообщений
```

## Реализация

### Структура сообщения (message_entity.py)

```python
from dataclasses import dataclass

@dataclass
class Message:
    id: str
    msg: str
```

**Назначение:**
- Хранение идентификатора отправителя
- Хранение текста сообщения
- Удобная сериализация в JSON

### Серверная часть (server.py)

```python
import socket
import threading
import json

HOST = "127.0.0.1"
PORT = 8082

clients = {}  # id -> conn
clients_lock = threading.Lock()

def handle_client(conn, addr):
    try:
        # First message should be client id (simple protocol)
        client_id = conn.recv(1024).decode().strip()
        if not client_id:
            conn.close()
            return

        with clients_lock:
            if client_id in clients:
                conn.sendall(b"ID_USED")
                conn.close()
                return
            clients[client_id] = conn
        print("Client connected:", client_id, addr)
        while True:
            data = conn.recv(4096)
            if not data:
                break
            text = data.decode().strip()
            print(f"Received from {client_id}: {text}")
            msg_obj = {"id": client_id, "msg": text}
            broadcast(json.dumps(msg_obj))
    finally:
        with clients_lock:
            # remove
            for k, v in list(clients.items()):
                if v is conn:
                    del clients[k]
                    break
        conn.close()
        print("Client disconnected:", client_id)

def broadcast(message: str):
    with clients_lock:
        for cid, cconn in list(clients.items()):
            try:
                cconn.sendall(message.encode())
            except Exception:
                # ignore send errors, remove later in recv loop
                pass

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Chat server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
```

**Ключевые компоненты:**

1. **Глобальное хранилище клиентов**
   - `clients = {}` - словарь id -> connection
   - `clients_lock` - мьютекс для синхронизации доступа
   
2. **Функция handle_client**
   - Получение ID клиента при подключении
   - Проверка уникальности ID
   - Цикл чтения сообщений
   - Очистка при отключении
   
3. **Функция broadcast**
   - Рассылка сообщения всем клиентам
   - Обработка ошибок отправки
   - Thread-safe с использованием lock
   
4. **Главный цикл**
   - Прием новых подключений
   - Создание нового потока для каждого клиента
   - Daemon потоки завершаются при закрытии программы

### Клиентская часть (client.py)

```python
import socket
import threading
import json

HOST = "127.0.0.1"
PORT = 8082

def recv_loop(s):
    while True:
        data = s.recv(4096)
        if not data:
            break
        try:
            msg = json.loads(data.decode())
            print(f"[{msg['id']}] {msg['msg']}")
        except Exception:
            print("Received:", data.decode())

def send_loop(s):
    while True:
        try:
            text = input()
            if not text:
                continue
            s.sendall(text.encode())
        except EOFError:
            break

def main():
    user_id = input("Enter your id: ").strip()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(user_id.encode())

    threading.Thread(target=recv_loop, args=(s,), daemon=True).start()
    send_loop(s)
    s.close()

if __name__ == "__main__":
    main()
```

**Ключевые компоненты:**

1. **Функция recv_loop**
   - Работает в отдельном потоке
   - Постоянно слушает сообщения от сервера
   - Парсит JSON и выводит на экран
   
2. **Функция send_loop**
   - Работает в основном потоке
   - Читает ввод пользователя
   - Отправляет сообщения на сервер
   
3. **Разделение приема и отправки**
   - Позволяет одновременно читать и писать
   - Не блокирует интерфейс при ожидании сообщений

## Запуск приложения

### Шаг 1: Запуск сервера

```bash
cd task4
python server.py
```

Ожидаемый вывод:
```
Chat server listening on 127.0.0.1:8082
```

### Шаг 2: Запуск первого клиента (в новом терминале)

```bash
cd task4
python client.py
```

```
Enter your id: Alice
```

### Шаг 3: Запуск второго клиента (в еще одном терминале)

```bash
cd task4
python client.py
```

```
Enter your id: Bob
```

### Шаг 4: Отправка сообщений

**Alice:**
```
Hello everyone!
```

**Bob увидит:**
```
[Alice] Hello everyone!
```

**Bob:**
```
Hi Alice!
```

**Alice увидит:**
```
[Bob] Hi Alice!
```

## Диаграмма работы

```
Client A          Server           Client B
   |                 |                 |
   |-- connect() --->|                 |
   |<- accept() -----|                 |
   |-- send("A") --->|                 |
   |                 |<--- connect() --|
   |                 |---- accept() -->|
   |                 |<--- send("B") --|
   |                 |                 |
   |- send("Hi!") -->|                 |
   |                 |-- broadcast --->|
   |                 |                 [print "A: Hi!"]
   |                 |                 |
   |                 |<- send("Hello")-|
   |                 |-- broadcast --->|
   [print "B: Hello"]|                 |
```

## Потокобезопасность (Thread Safety)

### Проблемы многопоточности

1. **Race Conditions** - конкурентный доступ к общим данным
2. **Deadlocks** - взаимная блокировка потоков
3. **Inconsistent State** - несогласованное состояние данных

### Решения в нашей реализации

```python
clients_lock = threading.Lock()

# Защита критической секции
with clients_lock:
    clients[client_id] = conn
```

**Преимущества Lock:**
- Гарантирует атомарность операций
- Предотвращает race conditions
- Context manager автоматически освобождает блокировку

## Особенности реализации

!!! success "Многопоточность"
    Каждый клиент обрабатывается в отдельном потоке, позволяя серверу работать с множеством пользователей одновременно

!!! info "JSON протокол"
    Использование JSON для структурированной передачи данных

!!! warning "Daemon потоки"
    Потоки помечены как daemon, они автоматически завершаются при выходе из программы

!!! note "Уникальность ID"
    Сервер проверяет уникальность идентификатора и отклоняет дубликаты

## Протокол обмена

1. **Подключение:**
   - Клиент подключается к серверу
   - Отправляет свой ID как первое сообщение
   
2. **Регистрация:**
   - Сервер проверяет уникальность ID
   - Добавляет клиента в список или отклоняет
   
3. **Обмен сообщениями:**
   - Клиент отправляет текст
   - Сервер оборачивает в JSON: `{"id": "Alice", "msg": "text"}`
   - Рассылает всем клиентам
   
4. **Отключение:**
   - При разрыве соединения клиент удаляется из списка

## Масштабируемость

### Текущие ограничения

- Все клиенты в одном процессе
- Ограничено количеством потоков
- Нет персистентности сообщений
- Нет комнат/каналов

### Возможные улучшения

1. **Комнаты чата**
   ```python
   rooms = {"general": [], "tech": []}
   ```

2. **История сообщений**
   ```python
   message_history = []
   ```

3. **Приватные сообщения**
   ```python
   {"to": "Alice", "from": "Bob", "msg": "Secret"}
   ```

4. **Команды**
   ```python
   /join room_name
   /list
   /quit
   ```

5. **Аутентификация**
   - Проверка пароля
   - Токены доступа

## Сравнение подходов

| Подход | Преимущества | Недостатки |
|--------|--------------|------------|
| Threading | Простота, подходит для I/O | GIL, ограниченная масштабируемость |
| Asyncio | Высокая производительность | Сложнее в понимании |
| Multiprocessing | Истинная параллельность | Больше ресурсов, сложнее IPC |

## Тестирование

### Проверка уникальности ID

1. Запустить два клиента с одинаковым ID
2. Второй должен получить "ID_USED" и отключиться

### Проверка broadcast

1. Запустить 3+ клиентов
2. Отправить сообщение от одного
3. Все остальные должны получить его

### Проверка отключения

1. Закрыть одного клиента
2. Сервер должен вывести "Client disconnected"
3. Другие клиенты продолжают работать

## Выводы

В данном задании была реализована полноценная многопользовательская система обмена сообщениями. Продемонстрированы:
- Многопоточное программирование на Python
- Синхронизация доступа к общим ресурсам
- Broadcast рассылка сообщений
- Протокол регистрации клиентов
- Обработка подключений и отключений
- JSON для структурированной передачи данных

Эта реализация показывает принципы работы реальных чат-серверов и является основой для более сложных систем реального времени.
