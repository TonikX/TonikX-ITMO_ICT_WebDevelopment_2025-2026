# Установка и запуск (общие шаги)

## 1) Подготовка окружения
Проверь версию Python:
```bash
python3 --version
```

Перейди в папку лабораторной работы и (при желании) создай виртуальное окружение:
```bash
python3 -m venv venv
source venv/bin/activate
```

Для этой лабораторной **дополнительные зависимости не требуются** (всё на стандартной библиотеке Python).

## 2) Важное про порты
Если какой‑то порт занят, поменяй его в коде (константы `HOST`/`PORT`) и перезапусти сервер/клиент.

## 3) Запуск заданий
Каждое задание находится в своей папке `task*`.
Ниже — короткие команды запуска. Подробности — в разделе «Интерфейсы».

### Задание 1 (UDP)
```bash
cd task1_udp_hello
python server.py
```
В другом терминале:
```bash
python client.py
```

### Задание 2 (TCP, вариант 4)
```bash
cd task2_tcp_math
python server.py
```
В другом терминале:
```bash
python client.py
```

### Задание 3 (HTTP отдаёт index.html)
```bash
cd task3_http_file
python server.py
```
Открыть в браузере:
- http://127.0.0.1:8080/

### Задание 4 (многопользовательский чат TCP)
```bash
cd task4_chat_tcp_multiclient
python server.py
```
Далее запускаем клиентов в нескольких терминалах:
```bash
python client.py
```

### Задание 5 (HTTP GET/POST + журнал)
```bash
cd task5_http_journal
python server.py
```
Открыть в браузере:
- http://127.0.0.1:8081/
