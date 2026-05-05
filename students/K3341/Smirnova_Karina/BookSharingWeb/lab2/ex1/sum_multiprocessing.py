import multiprocessing as mp
import time

N = 10_000_000_000

def calculate_sum(args) -> int:
    start, end = args
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

def mp_sum(n: int, num_procs: int):
    ranges = chunk_ranges(n, num_procs)
    t0 = time.perf_counter()
    with mp.Pool(processes=num_procs) as pool:
        parts = pool.map(calculate_sum, ranges)
    t1 = time.perf_counter()
    return sum(parts), (t1 - t0)

def expected_sum(n: int) -> int:
    return n * (n + 1) // 2

if __name__ == "__main__":
    num_procs = min(8, mp.cpu_count())

    total, seconds = mp_sum(N, num_procs)
    exp = expected_sum(N)

    print(f"[multiprocessing] procs={num_procs} time={seconds:.6f}s")
    print(f"[multiprocessing] correct={total == exp}")

# result:
# [multiprocessing] procs=6 time=1.155195s
# [multiprocessing] correct=True