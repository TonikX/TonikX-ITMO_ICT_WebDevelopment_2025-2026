# Лабораторная работа №2 (2 семестр) — Потоки, процессы, асинхронность

**Цель:** разобраться в отличиях между `threading`, `multiprocessing` и `asyncio` в Python, понять когда какой подход эффективен.

## Состав

- **Задание 1.** Параллельное суммирование чисел `1..N` — классическая CPU-bound задача. Позволяет увидеть эффект GIL: `threading` не даёт ускорения, `multiprocessing` — даёт, `asyncio` бесполезен для чистого CPU.
- **Задание 2.** Параллельный парсинг веб-страниц с сохранением заголовков в БД — I/O-bound задача. Здесь, наоборот, выигрывают `threading` и `asyncio`, а `multiprocessing` проигрывает из-за накладных расходов на старт процессов.

## Исходный код

Каталог лабораторной: `students/k3340/Sobol_Vladimir/lab2_sem2/`.

```
lab2_sem2/
├── task1/
│   ├── threading_sum.py
│   ├── multiprocessing_sum.py
│   ├── async_sum.py
│   └── benchmark.py
├── task2/
│   ├── db.py              # SQLModel + SQLite
│   ├── urls.py            # список URL
│   ├── threading_parser.py
│   ├── multiprocessing_parser.py
│   ├── async_parser.py
│   └── benchmark.py
├── requirements.txt
└── README.md
```

## Выводы одной строкой

| Задача       | Победитель        | Почему                                                         |
|--------------|-------------------|----------------------------------------------------------------|
| CPU-bound    | `multiprocessing` | обходит GIL — реальное параллельное выполнение на ядрах CPU    |
| I/O-bound    | `asyncio`         | один поток + кооперативное переключение, минимум оверхеда      |
