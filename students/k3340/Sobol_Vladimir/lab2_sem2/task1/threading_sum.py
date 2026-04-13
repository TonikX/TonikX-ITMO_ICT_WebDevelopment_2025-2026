"""Суммирование 1..N с помощью threading."""
import threading
import time
from typing import List

N = 10 ** 8
WORKERS = 4


def calculate_sum(start: int, end: int, out: List[int], idx: int) -> None:
    s = 0
    for i in range(start, end + 1):
        s += i
    out[idx] = s


def run() -> tuple[int, float]:
    chunk = N // WORKERS
    results = [0] * WORKERS
    threads: list[threading.Thread] = []

    t0 = time.perf_counter()
    for i in range(WORKERS):
        start = i * chunk + 1
        end = N if i == WORKERS - 1 else (i + 1) * chunk
        t = threading.Thread(target=calculate_sum, args=(start, end, results, i))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    elapsed = time.perf_counter() - t0
    return sum(results), elapsed


if __name__ == "__main__":
    total, elapsed = run()
    expected = N * (N + 1) // 2
    print(f"threading  N={N}  workers={WORKERS}  sum={total}  ok={total == expected}  time={elapsed:.3f}s")
