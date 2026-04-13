# Задание 2 — Параллельный парсинг веб-страниц

## Постановка

Параллельно загрузить список URL-адресов, распарсить `<title>` каждой страницы и сохранить его в БД — тремя способами (`threading`, `multiprocessing`, `asyncio`). Замерить и сравнить время.

## База данных

Чтобы отчёт можно было воспроизвести без поднятия PostgreSQL, в качестве хранилища взят SQLite (файл `task2/parsed_pages.db`). Схема описана в `task2/db.py` через SQLModel — той же библиотекой, что использовалась в Лабораторной работе №1 (2 семестр):

```python
class ParsedPage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str = Field(index=True)
    title: str
    approach: str                # threading / multiprocessing / async
    fetched_at: datetime = Field(default_factory=datetime.utcnow)
```

Функция `save_page(url, title, approach)` открывает короткоживущую сессию и коммитит одну запись.

## Список URL (`task2/urls.py`)

12 страниц: `example.com`, `python.org`, `docs.python.org`, `pypi.org`, несколько статей Википедии (Python, Concurrency, Multiprocessing, Thread, Async I/O, GIL), `fastapi.tiangolo.com`, `djangoproject.com`.

## Реализация

Все три варианта определяют `parse_and_save(url)`: скачивает HTML, вытаскивает `<title>` через BeautifulSoup, пишет в БД, печатает строку в консоль. Сетевые ошибки ловятся и сохраняются в поле `title` как `<error: ClassName>` — чтобы сравнение не ломалось из-за одного «битого» URL.

### `threading_parser.py`

```python
threads = [threading.Thread(target=parse_and_save, args=(u,)) for u in URLS]
for t in threads: t.start()
for t in threads: t.join()
```

### `multiprocessing_parser.py`

```python
with mp.Pool(processes=min(len(URLS), 8)) as pool:
    pool.map(parse_and_save, URLS)
```

### `async_parser.py`

Используется `aiohttp` вместо `requests`, т.к. `requests` — блокирующая библиотека и в `asyncio` без executor-а смысла не имеет.

```python
async with aiohttp.ClientSession(headers=headers) as session:
    await asyncio.gather(*(parse_and_save(session, u) for u in URLS))
```

## Результаты

Замер на домашнем Wi-Fi, 12 URL (`task2/benchmark.py`):

| Подход            | Время, с |
|-------------------|----------|
| `threading`       | 1.540    |
| `multiprocessing` | 3.290    |
| `asyncio`         | **1.141** |

## Анализ

- **Задача I/O-bound.** Основное время программа ждёт ответа от сервера — CPU почти простаивает, и GIL из минуса превращается в нейтральный фактор.
- **`threading` даёт близкий к async результат.** Пока один поток ждёт `recv`, ОС переключает GIL на другой — параллелизм по сетевым запросам получается, несмотря на GIL.
- **`asyncio` — самый быстрый и лёгкий.** Один поток + event loop переключает корутины по `await`; нет накладных расходов на ОС-потоки и переключения контекста ядра.
- **`multiprocessing` проигрывает.** Для 12 HTTP-запросов стоимость старта пула процессов, сериализации аргументов и результата превышает выигрыш от «параллелизма» — его тут и так не требовалось, т.к. задача не CPU-bound.
- **Вывод.** Для параллельных сетевых запросов в Python разумный выбор — `asyncio`/`aiohttp` или `threading`; `multiprocessing` имеет смысл только если к запросам добавляется тяжёлая CPU-обработка ответов.

## Проверка БД

После запуска `benchmark.py` в `task2/parsed_pages.db` появляется по записи на каждый `(url, approach)`:

```sql
sqlite> SELECT approach, COUNT(*) FROM parsedpage GROUP BY approach;
async|12
multiprocessing|12
threading|12
```

## Сводное сравнение с Заданием 1

| Тип задачи | Победитель        | Аутсайдер         |
|------------|-------------------|-------------------|
| CPU-bound  | `multiprocessing` | `threading` / `async` |
| I/O-bound  | `asyncio`         | `multiprocessing` |

Итог: «универсально лучшего» подхода нет — выбор определяется природой задачи.
