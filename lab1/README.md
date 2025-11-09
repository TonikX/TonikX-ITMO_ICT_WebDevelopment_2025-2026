### Задание 1 (UDP)
Сервер:
```bash
python task1_udp/server_udp.py
```
Клиент:
```bash
python task1_udp/client_udp.py
```

### Задание 2 (TCP, математика)
Сервер:
```bash
python task2_tcp_math/server_tcp_math.py
```
Клиент:
```bash
python task2_tcp_math/client_tcp_math.py
```
Примеры команд на клиенте:
```
pythagoras 3 4
quadratic 1 -3 2
trapezoid 3 5 2
parallelogram 10 7
exit
```

### Задание 3 (HTTP из файла)
Сервер:
```bash
cd task3_http_file
python http_file_server.py
```
Откройте в браузере: `http://localhost:8088/`

### Задание 4 (Многопользовательский чат, TCP + threading)
Сервер:
```bash
python task4_chat/server_chat.py
```
Клиент (в разных терминалах несколько раз):
```bash
python task4_chat/client_chat.py
```

### Задание 5 (Мини веб-сервер: GET/POST)
Сервер:
```bash
python task5_web_server/grades_server.py
```
Откройте `http://localhost:8089/`, добавляйте записи через форму. Данные сохраняются в `grades.json`.

