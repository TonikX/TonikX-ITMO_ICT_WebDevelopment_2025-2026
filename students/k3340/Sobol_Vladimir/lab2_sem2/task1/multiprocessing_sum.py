"""Суммирование 1..N с помощью multiprocessing."""
import multiprocessing as mp
import time

N = 10 ** 8
WORKERS = 4


def calculate_sum(bounds: tuple[int, int]) -> int:
    start, end = bounds
    s = 0
    for i in range(start, end + 1):
        s += i
    return s


def run() -> tuple[int, float]:
    chunk = N // WORKERS
    ranges = []
    for i in range(WORKERS):
        start = i * chunk + 1
        end = N if i == WORKERS - 1 else (i + 1) * chunk
        ranges.append((start, end))

    t0 = time.perf_counter()
    with mp.Pool(processes=WORKERS) as pool:
        parts = pool.map(calculate_sum, ranges)
    elapsed = time.perf_counter() - t0
    return sum(parts), elapsed


if __name__ == "__main__":
    total, elapsed = run()
    expected = N * (N + 1) // 2
    print(f"multiprocessing  N={N}  workers={WORKERS}  sum={total}  ok={total == expected}  time={elapsed:.3f}s")
