"""Суммирование 1..N с помощью asyncio.

CPU-bound задача не ускоряется корутинами: asyncio — кооперативная
многозадачность в одном потоке, GIL всё равно активен. Здесь подзадачи
пакуются в asyncio.gather, чтобы показать интерфейс, но выполняются
последовательно на одном event loop.
"""
import asyncio
import time

N = 10 ** 8
WORKERS = 4


async def calculate_sum(start: int, end: int) -> int:
    s = 0
    for i in range(start, end + 1):
        s += i
    return s


async def main() -> tuple[int, float]:
    chunk = N // WORKERS
    tasks = []
    for i in range(WORKERS):
        start = i * chunk + 1
        end = N if i == WORKERS - 1 else (i + 1) * chunk
        tasks.append(calculate_sum(start, end))

    t0 = time.perf_counter()
    parts = await asyncio.gather(*tasks)
    elapsed = time.perf_counter() - t0
    return sum(parts), elapsed


if __name__ == "__main__":
    total, elapsed = asyncio.run(main())
    expected = N * (N + 1) // 2
    print(f"async  N={N}  workers={WORKERS}  sum={total}  ok={total == expected}  time={elapsed:.3f}s")
