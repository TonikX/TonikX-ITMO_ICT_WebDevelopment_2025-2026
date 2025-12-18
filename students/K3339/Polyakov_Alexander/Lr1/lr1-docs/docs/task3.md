# Задача 3 - HTTP сервер для статических файлов

## Цель

Реализация простого HTTP сервера для обслуживания статических HTML файлов с изучением основ веб-технологий и HTTP протокола.

## Выполненная работа

Был создан HTTP сервер, который принимает GET запросы, проверяет наличие файла `index.html` и возвращает его содержимое с соответствующими HTTP заголовками. 

Сервер формирует правильные HTTP/1.1 ответы с обязательными заголовками:

```python
def build_response(status: str, body: bytes, content_type: str = "text/html; charset=utf-8") -> bytes:
    lines = [
        f"HTTP/1.1 {status}",
        f"Date: {formatdate(timeval=None, usegmt=True)}",
        "Server: MinimalSocketServer/1.0",
        f"Content-Length: {len(body)}",
        f"Content-Type: {content_type}",
        "Connection: close",
        "", ""
    ]
    headers = "\r\n".join(lines).encode("ascii")
    return headers + body
```

Реализована обработка двух случаев: успешное обслуживание файла (200 OK) и отсутствие файла (404 Not Found).

## Результат

Успешно создан HTTP сервер, обслуживающий статические файлы. Изучены особенности HTTP протокола как прикладного уровня над TCP, включая формат запросов/ответов, стандартизированные заголовки и семантику веб-взаимодействия.