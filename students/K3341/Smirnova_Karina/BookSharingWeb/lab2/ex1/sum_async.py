import asyncio
import time

N = 10_000_000_000

def calculate_sum(start: int, end: int) -> int:
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

async def async_worker(start: int, end: int) -> int:
    return calculate_sum(start, end)

async def async_sum(n: int, num_tasks: int):
    ranges = chunk_ranges(n, num_tasks)
    t0 = time.perf_counter()
    tasks = [asyncio.create_task(async_worker(s, e)) for (s, e) in ranges]
    parts = await asyncio.gather(*tasks)
    t1 = time.perf_counter()
    return sum(parts), (t1 - t0)

def expected_sum(n: int) -> int:
    return n * (n + 1) // 2

if __name__ == "__main__":
    num_tasks = 8

    total, seconds = asyncio.run(async_sum(N, num_tasks))
    exp = expected_sum(N)

    print(f"[asyncio] tasks={num_tasks} time={seconds:.6f}s")
    print(f"[asyncio] correct={total == exp}")

# result:
# [asyncio] tasks=8 time=0.000589s
# [asyncio] correct=True