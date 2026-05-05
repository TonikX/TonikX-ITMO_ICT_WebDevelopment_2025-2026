import threading
import time

N = 10_000_000_000_000

def calculate_sum(start: int, end: int) -> int:
    sum = 0
    count = end - start + 1
    return (start + end) * count // 2

def chunk_ranges(n: int, chunks: int):
    size = n // chunks
    ranges = []
    s = 1
    for i in range(chunks):
        e = s + size - 1
        if i == chunks - 1:
            e = n
        ranges.append((s, e))
        s = e + 1
    return ranges

def threaded_sum(n: int, num_threads: int) -> tuple[int, float]:
    ranges = chunk_ranges(n, num_threads)
    results = [0] * num_threads
    threads = []

    def worker(i: int, start: int, end: int):
        results[i] = calculate_sum(start, end)

    for i, (start, end) in enumerate(ranges):
        t = threading.Thread(target=worker, args=(i, start, end))
        threads.append(t)

    t0 = time.perf_counter()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    t1 = time.perf_counter()

    total = sum(results)
    return total, (t1 - t0)

def expected_sum(n: int) -> int:
    return n * (n + 1) // 2

if __name__ == "__main__":
    num_threads = 8

    total, seconds = threaded_sum(N, num_threads)
    exp = expected_sum(N)

    print(f"[threading] threads={num_threads} time={seconds:.6f}s")
    print(f"[threading] correct={total == exp}")

# result:
# [threading] threads=8 time=0.011124s
# [threading] correct=True