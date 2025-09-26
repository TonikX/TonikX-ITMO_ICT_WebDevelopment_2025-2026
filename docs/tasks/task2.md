# Задание 2: TCP Математические операции

## Описание задания

Реализовать клиентскую и серверную часть приложения. Клиент запрашивает выполнение математической операции, параметры которой вводятся с клавиатуры. Сервер обрабатывает данные и возвращает результат клиенту.

## Требования

- Использование библиотеки `socket`
- Реализация с помощью протокола TCP
- 4 математические операции на выбор

## Варианты операций

1. **Теорема Пифагора** - вычисление гипотенузы по двум катетам
2. **Решение квадратного уравнения** - нахождение корней уравнения ax² + bx + c = 0
3. **Площадь трапеции** - вычисление по формуле S = (a + b) × h / 2
4. **Площадь параллелограмма** - вычисление по формуле S = a × h

## Техническая реализация

### TCP Математический сервер

```python
import socket
import json
import math

def tcp_math_server():
    # Создание TCP сокета
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 12346))
    server_socket.listen(1)
    
    while True:
        client_socket, addr = server_socket.accept()
        
        try:
            # Получение запроса от клиента
            data = client_socket.recv(1024)
            request = json.loads(data.decode('utf-8'))
            
            operation = request['operation']
            params = request['params']
            
            # Обработка различных операций
            if operation == 1:  # Теорема Пифагора
                a, b = params['a'], params['b']
                result = math.sqrt(a**2 + b**2)
                response = f"Гипотенуза: {result:.2f}"
                
            elif operation == 2:  # Квадратное уравнение
                a, b, c = params['a'], params['b'], params['c']
                discriminant = b**2 - 4*a*c
                if discriminant >= 0:
                    x1 = (-b + math.sqrt(discriminant)) / (2*a)
                    x2 = (-b - math.sqrt(discriminant)) / (2*a)
                    response = f"Корни: x1={x1:.2f}, x2={x2:.2f}"
                else:
                    response = "Нет действительных корней"
            
            # Отправка результата клиенту
            client_socket.send(response.encode('utf-8'))
            
        except Exception as e:
            error_response = f"Ошибка: {str(e)}"
            client_socket.send(error_response.encode('utf-8'))
        finally:
            client_socket.close()
```

### TCP Математический клиент

```python
import socket
import json

def tcp_math_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12346))
    
    # Выбор операции
    print("Выберите операцию:")
    print("1. Теорема Пифагора")
    print("2. Квадратное уравнение")
    print("3. Площадь трапеции")
    print("4. Площадь параллелограмма")
    
    operation = int(input("Введите номер операции: "))
    
    # Ввод параметров в зависимости от операции
    if operation == 1:  # Теорема Пифагора
        a = float(input("Введите катет a: "))
        b = float(input("Введите катет b: "))
        params = {'a': a, 'b': b}
    
    # Формирование запроса
    request = {'operation': operation, 'params': params}
    
    # Отправка запроса
    client_socket.send(json.dumps(request).encode('utf-8'))
    
    # Получение ответа
    response = client_socket.recv(1024).decode('utf-8')
    print(f"Результат: {response}")
    
    client_socket.close()
```

## Математические формулы

### 1. Теорема Пифагора
```
c = √(a² + b²)
```

### 2. Квадратное уравнение
```
x = (-b ± √(b² - 4ac)) / 2a
```

### 3. Площадь трапеции
```
S = (a + b) × h / 2
```

### 4. Площадь параллелограмма
```
S = a × h
```

## Запуск

### Отдельные компоненты

```bash
# Запуск сервера
python task2_tcp_math.py server

# Запуск клиента (в другом терминале)
python task2_tcp_math.py client

# Демонстрация
python task2_tcp_math.py demo
```

### Через главное меню

```bash
python main.py
# Выберите пункт 2
```

## Особенности реализации

- **Модульность** - каждая операция обрабатывается отдельно
- **Расширяемость** - легко добавить новые математические операции
- **Валидация** - проверка корректности входных данных
- **Форматирование** - округление результатов до 2 знаков после запятой
