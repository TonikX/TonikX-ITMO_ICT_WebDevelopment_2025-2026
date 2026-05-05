import time
import asyncio
import aiohttp

from parser import parse
from urls_25 import URLS_25
from output_format import format_record

OUT_FILE = "async_results.txt"

async def parse_and_save(url: str, http: aiohttp.ClientSession, sem: asyncio.Semaphore, lock: asyncio.Lock):
    async with sem:
        async with http.get(url, timeout=aiohttp.ClientTimeout(total=20),
                            headers={"User-Agent": "Mozilla/5.0 (student parser)"}) as resp:
            resp.raise_for_status()
            html = await resp.text()

    data = parse(html)
    text = format_record(url, data)

    async with lock:
        with open(OUT_FILE, "a", encoding="utf-8") as f:
            f.write(text)

    print(f"[async] saved: {url} -> {data['title']}")

async def main_async():
    open(OUT_FILE, "w", encoding="utf-8").close()

    urls = URLS_25[:25]
    concurrency = 5
    sem = asyncio.Semaphore(concurrency)
    lock = asyncio.Lock()

    t0 = time.perf_counter()
    async with aiohttp.ClientSession() as http:
        tasks = [asyncio.create_task(parse_and_save(url, http, sem, lock)) for url in urls]
        await asyncio.gather(*tasks)
    t1 = time.perf_counter()

    print(f"[asyncio->file] urls={len(urls)} concurrency={concurrency} time={t1 - t0:.6f}s output={OUT_FILE}")

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()